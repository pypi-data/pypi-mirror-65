from asr.core import command


@command(dependencies=['asr.gs'],
         creates=['gllbsc.gpw'])
def calculate():
    from gpaw import GPAW, FermiDirac
    calc = GPAW('gs.gpw', txt=None)
    atoms = calc.get_atoms()

    if atoms.get_initial_magnetic_moments().any():
        raise AssertionError('GLLB-SC does not work with mag moms')
    dct = calc.todict()
    dct.update(fixdensity=False, txt='gllbsc.txt', xc='GLLBSC',
               parallel={'band': 1},
               occupations=FermiDirac(width=0.01))
    calc = GPAW(**dct)
    atoms.set_calculator(calc)
    atoms.get_potential_energy()
    response = atoms.calc.hamiltonian.xc.xcs['RESPONSE']
    response.calculate_delta_xc()
    Eks, deltaxc = response.calculate_delta_xc_perturbation()
    atoms.calc.write('gllbsc.gpw')
    v = atoms.calc.get_electrostatic_potential()
    evac = v[:, :, 0].mean()
    results = {'deltaxc': deltaxc,
               'evac': evac}
    return results


@command(requires=['gllbsc.gpw'],
         dependencies=['asr.gllbsc@calculate'])
def main():
    import numpy as np
    from ase.dft.bandgap import bandgap
    from gpaw import GPAW
    from gpaw.spinorbit import get_spinorbit_eigenvalues
    from gpaw.mpi import serial_comm
    from asr.core import read_json
    from asr.utils.gpw2eigs import (eigenvalues, get_spin_direction,
                                    fermi_level)
    
    dct = read_json('results-asr.gllbsc@calculate.json')
    deltaxc = dct['deltaxc']
    # write gaps
    calc = GPAW('gllbsc.gpw', communicator=serial_comm, txt=None)
    eps_kn = eigenvalues(calc)[0]
    eps_kn[eps_kn > calc.get_fermi_level()] += deltaxc
    efermi_nosoc = calc.get_fermi_level()
    gap_nosoc, p1, p2 = bandgap(eigenvalues=eps_kn, efermi=efermi_nosoc,
                                output=None)
    results = {}
    if gap_nosoc > 0:
        results.update(vbm_gllbsc_nosoc=eps_kn[p1],
                       cbm_gllbsc_nosoc=eps_kn[p2])
    dir_gap_nosoc, p1, p2 = bandgap(eigenvalues=eps_kn,
                                    efermi=efermi_nosoc,
                                    direct=True, output=None)
    theta, phi = get_spin_direction()
    eps_km = get_spinorbit_eigenvalues(calc, gw_kn=eps_kn,
                                       theta=theta, phi=phi).transpose()
    efermi = fermi_level(calc, eps_km[np.newaxis],
                         nelectrons=2 * calc.get_number_of_electrons())
    gap, p1, p2 = bandgap(eigenvalues=eps_km, efermi=efermi, output=None)
    if gap > 0:
        results.update(vbm_gllbsc=eps_km[p1],
                       cbm_gllbsc=eps_km[p2])
    dir_gap, p1, p2 = bandgap(eigenvalues=eps_km, efermi=efermi,
                              direct=True, output=None)
    results.update({'gap_gllbsc': gap,
                    'dir_gap_gllbsc': dir_gap,
                    'gap_gllbsc_nosoc': gap_nosoc,
                    'dir_gap_gllbsc_nosoc': dir_gap_nosoc})
    return results


if __name__ == '__main__':
    main.cli()
