"""Relax an atomic structure.

By defaults read from "unrelaxed.json" from disk and relaxes
structures and saves the final relaxed structure in "structure.json".

The relax recipe has a couple of note-worthy features::

  - It automatically handles structures of any dimensionality
  - It tries to enforce symmetries
  - It continously checks after each step that no symmetries are broken,
    and raises an error if this happens.
"""

import numpy as np
from ase.io import read, write, Trajectory
from ase.io.formats import UnknownFileTypeError
from ase import Atoms
from ase.optimize.bfgs import BFGS

from asr.core import command, option
from math import sqrt
import time


class BrokenSymmetryError(Exception):
    pass


Uvalues = {}

# From [acs comb sci 2.011, 13, 383-390, Setyawan et al.]
UTM = {'Ti': 4.4, 'V': 2.7, 'Cr': 3.5, 'Mn': 4.0, 'Fe': 4.6,
       'Co': 5.0, 'Ni': 5.1, 'Cu': 4.0, 'Zn': 7.5, 'Ga': 3.9,
       'Nb': 2.1, 'Mo': 2.4, 'Tc': 2.7, 'Ru': 3.0, 'Rh': 3.3,
       'Pd': 3.6, 'Cd': 2.1, 'In': 1.9,
       'Ta': 2.0, 'W': 2.2, 'Re': 2.4, 'Os': 2.6, 'Ir': 2.8, 'Pt': 3.0}

for key, value in UTM.items():
    Uvalues[key] = ':d,{},0'.format(value)


def is_relax_done(atoms, fmax=0.01, smax=0.002,
                  smask=np.array([1, 1, 1, 1, 1, 1])):
    f = atoms.get_forces()
    s = atoms.get_stress() * smask
    done = (f**2).sum(1).max() <= fmax**2 and abs(s).max() <= smax

    return done


class SpgAtoms(Atoms):

    @classmethod
    def from_atoms(cls, atoms):
        # Due to technicalities we cannot mess with the __init__ constructor
        # -> therefore we make our own
        a = cls(atoms)
        a.set_symmetries([np.eye(3)], [[0, 0, 0]])
        return a

    def set_symmetries(self, symmetries, translations):
        self.t_sc = translations
        self.op_svv = [np.linalg.inv(self.cell).dot(op_cc.T).dot(self.cell) for
                       op_cc in symmetries]
        self.nsym = len(symmetries)
        tolerance = 1e-4
        spos_ac = self.get_scaled_positions()
        a_sa = []

        for op_cc, t_c in zip(symmetries, self.t_sc):
            symspos_ac = np.dot(spos_ac, op_cc.T) + t_c

            a_a = []
            for s_c in symspos_ac:
                diff_ac = spos_ac - s_c
                diff_ac -= np.round(diff_ac)
                mask_c = np.all(np.abs(diff_ac) < tolerance, axis=1)
                assert np.sum(mask_c) == 1, f'Bad symmetry, {mask_c}'
                ind = np.argwhere(mask_c)[0][0]
                assert ind not in a_a, f'Bad symmetry {ind}, {diff_ac}'
                a_a.append(ind)
            a_sa.append(a_a)

        self.a_sa = np.array(a_sa)

    def get_stress(self, voigt=True, *args, **kwargs):
        sigma0_vv = Atoms.get_stress(self, voigt=False, *args, **kwargs)

        sigma_vv = np.zeros((3, 3))
        for op_vv in self.op_svv:
            sigma_vv += np.dot(np.dot(op_vv, sigma0_vv), op_vv.T)
        sigma_vv /= self.nsym

        if voigt:
            return sigma_vv.flat[[0, 4, 8, 5, 2, 1]]

        return sigma_vv

    def get_forces(self, *args, **kwargs):
        f0_av = Atoms.get_forces(self, *args, **kwargs)
        f_av = np.zeros_like(f0_av)
        for map_a, op_vv in zip(self.a_sa, self.op_svv):
            for a1, a2 in enumerate(map_a):
                f_av[a2] += np.dot(f0_av[a1], op_vv)
        f_av /= self.nsym
        return f_av


class myBFGS(BFGS):

    def log(self, forces=None, stress=None):
        if forces is None:
            forces = self.atoms.atoms.get_forces()
        if stress is None:
            stress = self.atoms.atoms.get_stress()
        fmax = sqrt((forces**2).sum(axis=1).max())
        smax = abs(stress).max()
        e = self.atoms.get_potential_energy(
            force_consistent=self.force_consistent)
        T = time.localtime()
        if self.logfile is not None:
            name = self.__class__.__name__
            if self.nsteps == 0:
                self.logfile.write(' ' * len(name)
                                   + '  {:<4} {:<8} {:<10} '.format('Step',
                                                                    'Time',
                                                                    'Energy')
                                   + '{:<10} {:<10}\n'.format('fmax',
                                                              'smax'))
                if self.force_consistent:
                    self.logfile.write(
                        '*Force-consistent energies used in optimization.\n')
            fc = '*' if self.force_consistent else ''
            self.logfile.write(f'{name}: {self.nsteps:<4} '
                               f'{T[3]:02d}:{T[4]:02d}:{T[5]:02d} '
                               f'{e:<10.6f}{fc} {fmax:<10.4f} {smax:<10.4f}\n')
            self.logfile.flush()


def relax(atoms, name, emin=-np.inf, smask=None, dftd3=True,
          fixcell=False, allow_symmetry_breaking=False, dft=None,
          fmax=0.01, enforce_symmetry=False):
    import spglib

    if dftd3:
        from ase.calculators.dftd3 import DFTD3

    nd = int(np.sum(atoms.get_pbc()))
    if smask is None:
        if fixcell:
            smask = [0, 0, 0, 0, 0, 0]
        elif nd == 3:
            smask = [1, 1, 1, 1, 1, 1]
        elif nd == 2:
            smask = [1, 1, 0, 0, 0, 1]
        else:
            pbc = atoms.get_pbc()
            assert pbc[2], "1D periodic axis should be the last one."
            smask = [0, 0, 1, 0, 0, 0]

    from asr.setup.symmetrize import atomstospgcell as ats
    dataset = spglib.get_symmetry_dataset(ats(atoms),
                                          symprec=1e-4,
                                          angle_tolerance=0.1)
    spgname = dataset['international']
    number = dataset['number']
    nsym = len(dataset['rotations'])
    atoms = SpgAtoms.from_atoms(atoms)
    if enforce_symmetry:
        atoms.set_symmetries(symmetries=dataset['rotations'],
                             translations=dataset['translations'])
    if dftd3:
        calc = DFTD3(dft=dft)
    else:
        calc = dft
    atoms.calc = calc

    # We are fixing atom=0 to reduce computational effort
    from ase.constraints import ExpCellFilter
    filter = ExpCellFilter(atoms, mask=smask)
    try:
        trajfile = Trajectory(name + '.traj', 'a', atoms)
        opt = myBFGS(filter,
                     logfile=name + '.log',
                     trajectory=trajfile)

        # fmax=0 here because we have implemented our own convergence criteria
        runner = opt.irun(fmax=0)

        for _ in runner:
            # Check that the symmetry has not been broken
            newdataset = spglib.get_symmetry_dataset(ats(atoms),
                                                     symprec=1e-4,
                                                     angle_tolerance=0.1)
            spgname2 = newdataset['international']
            number2 = newdataset['number']
            nsym2 = len(newdataset['rotations'])
            msg = (f'The initial spacegroup was {spgname} {number} '
                   f'but it changed to {spgname2} {number2} during '
                   'the relaxation.')
            if (not allow_symmetry_breaking
               and number != number2 and nsym > nsym2):
                # Log the last step
                opt.log()
                opt.call_observers()
                errmsg = 'The symmetry was broken during the relaxation! ' + msg
                raise BrokenSymmetryError(errmsg)
            elif number != number2:
                print('Not an error: The spacegroup has changed during relaxation. '
                      + msg)
                spgname = spgname2
                number = number2
                nsym = nsym2
                if enforce_symmetry:
                    atoms.set_symmetries(symmetries=newdataset['rotations'],
                                         translations=newdataset['translations'])

            if is_relax_done(atoms, fmax=fmax, smax=0.002, smask=smask):
                opt.log()
                opt.call_observers()
                break
    finally:
        trajfile.close()
        if opt.logfile is not None:
            opt.logfile.close()
    return atoms


def BN_check():
    # Check that 2D-BN doesn't relax to its 3D form
    from asr.core import read_json
    results = read_json('results-asr.relax.json')
    assert results['c'] > 5


tests = []
testargs = ("{'mode':{'ecut':300,'dedecut':'estimate',...},"
            "'kpts':{'density':2,'gamma':True},...}")
tests.append({'description': 'Test relaxation of Si.',
              'tags': ['gitlab-ci'],
              'cli': ['asr run "setup.materials -s Si2"',
                      'ase convert materials.json unrelaxed.json',
                      f'asr run "relax -c {testargs}"',
                      'asr run database.fromtree',
                      'asr run "database.browser --only-figures"'],
              'results': [{'file': 'results-asr.relax.json',
                           'c': (3.88, 0.001)}]})
tests.append({'description': 'Test relaxation of Si (cores=2).',
              'cli': ['asr run "setup.materials -s Si2"',
                      'ase convert materials.json unrelaxed.json',
                      f'asr run -p 2 "relax -c {testargs}"',
                      'asr run database.fromtree',
                      'asr run "database.browser --only-figures"'],
              'results': [{'file': 'results-asr.relax.json',
                           'c': (3.88, 0.001)}]})
tests.append({'description': 'Test relaxation of 2D-BN.',
              'name': 'test_asr.relax_2DBN',
              'cli': ['asr run "setup.materials -s BN,natoms=2"',
                      'ase convert materials.json unrelaxed.json',
                      f'asr run "relax -c {testargs}"',
                      'asr run database.fromtree',
                      'asr run "database.browser --only-figures"'],
              'test': BN_check})


def log(*args, **kwargs):
    atoms = read('unrelaxed.json')

    return {'atoms': atoms.todict()}


@command('asr.relax',
         requires=['unrelaxed.json'],
         creates=['structure.json'],
         log=log)
@option('-c', '--calculator', help='Calculator and its parameters.')
@option('--d3/--nod3', help='Relax with vdW D3')
@option('--fixcell', is_flag=True, help='Don\'t relax stresses')
@option('--allow-symmetry-breaking', is_flag=True,
        help='Allow symmetries to be broken during relaxation')
@option('--fmax', help='Maximum force allowed')
@option('--enforce-symmetry', is_flag=True,
        help='Symmetrize forces and stresses.')
def main(calculator={'name': 'gpaw',
                     'mode': {'name': 'pw', 'ecut': 800},
                     'xc': 'PBE',
                     'kpts': {'density': 6.0, 'gamma': True},
                     'basis': 'dzp',
                     'symmetry': {'symmorphic': False},
                     'convergence': {'forces': 1e-4},
                     'txt': 'relax.txt',
                     'occupations': {'name': 'fermi-dirac',
                                     'width': 0.05},
                     'charge': 0},
         d3=False, fixcell=False, allow_symmetry_breaking=False,
         fmax=0.01, enforce_symmetry=True):
    """Relax atomic positions and unit cell.

    By default, this recipe takes the atomic structure in
    'unrelaxed.json' and relaxes the structure including the DFTD3 van
    der Waals correction. The relaxed structure is saved to
    `structure.json` which can be processed by other recipes.

    To install DFTD3 do::

      $ mkdir ~/DFTD3 && cd ~/DFTD3
      $ wget chemie.uni-bonn.de/pctc/mulliken-center/software/dft-d3/dftd3.tgz
      $ tar -zxf dftd3.tgz
      $ make
      $ echo 'export ASE_DFTD3_COMMAND=$HOME/DFTD3/dftd3' >> ~/.bashrc
      $ source ~/.bashrc

    Examples
    --------
    Relax without using DFTD3::

      $ ase build -x diamond Si unrelaxed.json
      $ asr run "relax --nod3"

    Relax using the LDA exchange-correlation functional::

      $ ase build -x diamond Si unrelaxed.json
      $ asr run "relax --calculator {'xc':'LDA',...}"

    """
    from ase.calculators.calculator import get_calculator_class

    try:
        atoms = read('relax.traj')
    except (IOError, UnknownFileTypeError):
        atoms = read('unrelaxed.json', parallel=False)

    calculatorname = calculator.pop('name')
    Calculator = get_calculator_class(calculatorname)

    # Some calculator specific parameters
    nd = int(np.sum(atoms.get_pbc()))
    if calculatorname == 'gpaw':
        if 'kpts' in calculator:
            from ase.calculators.calculator import kpts2kpts
            if 'density' in calculator['kpts']:
                kpts = kpts2kpts(calculator['kpts'], atoms=atoms)
                calculator['kpts'] = kpts
        if nd == 2:
            assert not atoms.get_pbc()[2], \
                ('The third unit cell axis should be aperiodic for '
                 'a 2D material!')
            calculator['poissonsolver'] = {'dipolelayer': 'xy'}

    calc = Calculator(**calculator)
    # Relax the structure
    atoms = relax(atoms, name='relax', dftd3=d3,
                  fixcell=fixcell,
                  allow_symmetry_breaking=allow_symmetry_breaking,
                  dft=calc, fmax=fmax, enforce_symmetry=enforce_symmetry)

    edft = calc.get_potential_energy(atoms)
    etot = atoms.get_potential_energy()

    cellpar = atoms.cell.cellpar()
    results = {'etot': etot,
               'edft': edft,
               'a': cellpar[0],
               'b': cellpar[1],
               'c': cellpar[2],
               'alpha': cellpar[3],
               'beta': cellpar[4],
               'gamma': cellpar[5],
               'spos': atoms.get_scaled_positions(),
               'symbols': atoms.get_chemical_symbols()}

    # Calculator specific metadata
    if calculatorname == 'gpaw':
        # Get setup fingerprints
        fingerprint = {}
        for setup in calc.setups:
            fingerprint[setup.symbol] = setup.fingerprint
        results['__log__'] = {'nvalence': calc.setups.nvalence,
                              'setup_fingerprints__': fingerprint}

    results['__key_descriptions__'] = \
        {'etot': 'Total energy [eV]',
         'edft': 'DFT total energy [eV]',
         'spos': 'Array: Scaled positions',
         'symbols': 'Array: Chemical symbols',
         'a': 'Cell parameter a [Ang]',
         'b': 'Cell parameter b [Ang]',
         'c': 'Cell parameter c [Ang]',
         'alpha': 'Cell parameter alpha [deg]',
         'beta': 'Cell parameter beta [deg]',
         'gamma': 'Cell parameter gamma [deg]'}

    # For nm set magnetic moments to zero XXX
    # Save atomic structure
    write('structure.json', atoms)

    return results


if __name__ == '__main__':
    main.cli()
