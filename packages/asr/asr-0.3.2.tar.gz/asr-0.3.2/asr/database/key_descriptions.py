from asr.core import command, argument, get_recipes


# Style: "KVP: Long description !short description! [unit]

key_descriptions = {
    "berry": {"Topology": "KVP: Band topology !Topology!"},
    "bse": {"E_B": "KVP: Exciton binding energy from BSE "
            "!Exc. bind. energy! [eV]"},
    "convex_hull": {
        "ehull": "KVP: Energy above convex hull [eV/atom]",
        "hform": "KVP: Heat of formation [eV/atom]",
        "thermodynamic_stability_level": "KVP: Thermodynamic stability level",
    },
    "gs": {
        "forces": "Forces on atoms [eV/Angstrom]",
        "stresses": "Stress on unit cell [`eV/Angstrom^{dim-1}`]",
        "etot": "KVP: Total energy !Tot. En.! [eV]",
        "evac": "KVP: Vacuum level !Vacuum level! [eV]",
        "evacdiff":
        "KVP: Vacuum level difference !Vacuum level difference! [eV]",
        "dipz": "KVP: Out-of-plane dipole along +z axis [e * Ang]",
        "efermi": "KVP: Fermi level !Fermi level! [eV]",
        "gap": "KVP: Band gap !Band gap! [eV]",
        "vbm": "KVP: Valence band maximum !Val. band maximum! [eV]",
        "cbm": "KVP: Conduction band minimum !Cond. band maximum! [eV]",
        "gap_dir": "KVP: Direct band gap !Dir. band gap! [eV]",
        "gap_dir_nosoc":
        "KVP: Direct gap w/o soc. !Dir. gap wo. soc.! [eV]",
        "workfunction": "KVP: Work function (avg. if finite dipole) [eV]",
    },
    "gw": {
        "vbm_gw_nosoc": "Valence band maximum w/o soc. (GW) [eV]",
        "cbm_gw_nosoc": "Conduction band minimum w/o soc. (GW) [eV]",
        "gap_dir_gw_nosoc": "Direct gap w/o soc. (GW) [eV]",
        "gap_gw_nosoc": "Gap w/o soc. (GW) [eV]",
        "kvbm_nosoc": "k-point of GW valence band maximum w/o soc",
        "kcbm_nosoc": "k-point of GW conduction band minimum w/o soc",
        "vbm_gw": "KVP: Valence band maximum (GW) [eV]",
        "cbm_gw": "KVP: Conduction band minimum (GW) [eV]",
        "gap_dir_gw": "KVP: Direct band gap (GW) [eV]",
        "gap_gw": "KVP: Band gap (GW) [eV]",
        "kvbm": "k-point of GW valence band maximum",
        "kcbm": "k-point of GW conduction band minimum",
        "efermi_gw_nosoc": "Fermi energy w/o soc. (GW) [eV]",
        "efermi_gw_soc": "Fermi energy (GW) [eV]",
    },
    "hse": {
        "vbm_hse_nosoc": "Valence band maximum w/o soc. (HSE) [eV]",
        "cbm_hse_nosoc": "Conduction band minimum w/o soc. (HSE) [eV]",
        "gap_dir_hse_nosoc": "Direct gap w/o soc. (HSE) [eV]",
        "gap_hse_nosoc": "Band gap w/o soc. (HSE) [eV]",
        "kvbm_nosoc": "k-point of HSE valence band maximum w/o soc",
        "kcbm_nosoc": "k-point of HSE conduction band minimum w/o soc",
        "vbm_hse": "KVP: Valence band maximum (HSE) [eV]",
        "cbm_hse": "KVP: Conduction band minimum (HSE) [eV]",
        "gap_dir_hse": "KVP: Direct band gap (HSE) [eV]",
        "gap_hse": "KVP: Band gap (HSE) [eV]",
        "kvbm": "k-point of HSE valence band maximum",
        "kcbm": "k-point of HSE conduction band minimum",
        "efermi_hse_nosoc": "Fermi energy w/o soc. (HSE) [eV]",
        "efermi_hse_soc": "Fermi energy (HSE) [eV]",
    },
    "infraredpolarizability": {
        "alphax_lat": "KVP: Static lattice polarizability (x) [Ang]",
        "alphay_lat": "KVP: Static lattice polarizability (y) [Ang]",
        "alphaz_lat": "KVP: Static lattice polarizability (z) [Ang]",
        "alphax": "KVP: Static total polarizability (x) [Ang]",
        "alphay": "KVP: Static total polarizability (y) [Ang]",
        "alphaz": "KVP: Static total polarizability (z) [Ang]",
    },
    "magnetic_anisotropy": {
        "spin_axis": "KVP: Magnetic easy axis",
        "E_x": "KVP: Soc. total energy, x-direction [eV/unit cell]",
        "E_y": "KVP: Soc. total energy, y-direction [eV/unit cell]",
        "E_z": "KVP: Soc. total energy, z-direction [eV/unit cell]",
        "theta": "Easy axis, polar coordinates, theta [radians]",
        "phi": "Easy axis, polar coordinates, phi [radians]",
        "dE_zx":
        "KVP: Magnetic anisotropy energy between x and z axis [meV/unit cell]",
        "dE_zy":
        "KVP: Magnetic anisotropy energy between y and z axis [meV/unit cell]",
    },
    "pdos": {
        "pdos_nosoc":
        "Projected density of states w/o soc. !PDOS no soc!",
        "pdos_soc":
        "Projected density of states !PDOS!",
        "dos_at_ef_nosoc":
        "KVP: Density of states at the Fermi energy w/o soc."
        "!DOS at ef no soc.! [states/(eV * unit cell)]",
        "dos_at_ef_soc":
        "KVP: Density of states at the Fermi energy"
        " !DOS at ef! [states/(eV * unit cell)]",
    },
    "phonons": {
        "minhessianeig": "KVP: Minimum eigenvalue of Hessian [`eV/Ang^2`]",
        "dynamic_stability_level": "KVP: Dynamic stability level",
    },
    "plasmafrequency": {
        "plasmafreq_vv": "Plasma frequency tensor [Hartree]",
        "plasmafrequency_x": "KVP: 2D plasma frequency (x)"
        "[`eV/Ang^0.5`]",
        "plasmafrequency_y": "KVP: 2D plasma frequency (y)"
        "[`eV/Ang^0.5`]",
    },
    "polarizability": {
        "alphax_el": "KVP: Static electronic polarizability (x) [Ang]",
        "alphay_el": "KVP: Static electronic polarizability (y) [Ang]",
        "alphaz_el": "KVP: Static electronic polarizability (z) [Ang]",
    },
    "relax": {
        "etot": "Total energy [eV]",
        "edft": "DFT total enrgy [eV]",
        "spos": "Array: Scaled positions",
        "symbols": "Array: Chemical symbols",
        "a": "Cell parameter a [Ang]",
        "b": "Cell parameter b [Ang]",
        "c": "Cell parameter c [Ang]",
        "alpha": "Cell parameter alpha [deg]",
        "beta": "Cell parameter beta [deg]",
        "gamma": "Cell parameter gamma [deg]",
    },
    "stiffness": {
        "c_11": "KVP: Stiffness tensor, 11-component [`N/m^{dim-1}`]",
        "c_22": "KVP: Stiffness tensor, 22-component [`N/m^{dim-1}`]",
        "c_33": "KVP: Stiffness tensor, 33-component [`N/m^{dim-1}`]",
        "c_23": "KVP: Stiffness tensor, 23-component [`N/m^{dim-1}`]",
        "c_13": "KVP: Stiffness tensor, 13-component [`N/m^{dim-1}`]",
        "c_12": "KVP: Stiffness tensor, 12-component [`N/m^{dim-1}`]",
        "speed_of_sound_x": "KVP: Speed of sound (x) [m/s]",
        "speed_of_sound_y": "KVP: Speed of sound (y) [m/s]",
        "stiffness_tensor": "Stiffness tensor [`N/m^{dim-1}`]",
    },
    "structureinfo": {
        "magstate": "KVP: Magnetic state",
        "is_magnetic": "KVP: Material is magnetic !Magnetic!",
        "cell_area": "KVP: Area of unit-cell [`Ang^2`]",
        "has_inversion_symmetry": "KVP: Material has inversion symmetry",
        "stoichiometry": "KVP: Stoichiometry",
        "spacegroup": "KVP: Space group",
        "spgnum": "KVP: Space group number",
        "crystal_prototype": "KVP: Crystal prototype",
    },
    "database.material_fingerprint": {
        'asr_id': 'KVP: Material unique ID',
        'uid': 'KVP: Unique identifier'
    },
    "info.json": {
        'class': 'KVP: Material class',
        'doi': 'KVP: Monolayer reported DOI',
        'icsd_id': 'KVP: ICSD id of parent bulk structure',
        'cod_id': 'KVP: COD id of parent bulk structure'
    },
    "emasses": {
        'emass_vb_dir1':
        'KVP: Valence band effective mass, direction 1 [`m_e`]',
        'emass_vb_dir2':
        'KVP: Valence band effective mass, direction 2 [`m_e`]',
        'emass_vb_dir3':
        'KVP: Valence band effective mass, direction 3 [`m_e`]',
        'emass_cb_dir1':
        'KVP: Conduction band effective mass, direction 1 [`m_e`]',
        'emass_cb_dir2':
        'KVP: Conduction band effective mass, direction 2 [`m_e`]',
        'emass_cb_dir3':
        'KVP: Conduction band effective mass, direction 3 [`m_e`]',
    },
    "database.fromtree": {
        "folder": "KVP: Relative path to original folder",
    }
}

# Piezoelectrictensor key_descriptions
piezokd = {}
for i in range(1, 4):
    for j in range(1, 7):
        key = 'e_{}{}'.format(i, j)
        name = 'Piezoelectric tensor'
        description = f'Piezoelectric tensor {i}{j}-component' + '[`\\text{Ang}^{-1}`]'
        piezokd[key] = description

key_descriptions['piezoelectrictensor'] = piezokd

# Key descriptions like has_asr_gs_calculate
extras = {}
for recipe in get_recipes():
    key = 'has_' + recipe.name.replace('.', '_').replace('@', '_')
    extras[key] = f'{recipe.name} is calculated'

key_descriptions['extra'] = extras


@command()
@argument('database')
def main(database):
    """Analyze database and set metadata.

    This recipe loops through all rows in a database and figures out what keys
    are present in the database. It also figures our what kind of materials
    (1D, 2D, 3D) are in the database. Then it saves those values in the
    database metadata under {"keys": ["etot", "gap", ...]}
    """
    from ase.db import connect

    db = connect(database)

    print('Row #')
    keys = set()
    for ir, row in enumerate(db.select(include_data=False)):
        if ir % 100 == 0:
            print(ir)
        print(row.key_value_pairs.keys())
        keys.update(set(row.key_value_pairs.keys()))

    metadata = db.metadata
    metadata.update({'keys': sorted(list(keys))})
    db.metadata = metadata


if __name__ == '__main__':
    main.cli()
