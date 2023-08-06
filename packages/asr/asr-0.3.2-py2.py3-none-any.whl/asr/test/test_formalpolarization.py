import pytest
from .conftest import test_materials
import numpy as np
from ase import Atoms


@pytest.mark.ci
@pytest.mark.parametrize("atoms", test_materials)
def test_formalpolarization(separate_folder, mockgpaw, atoms):
    from asr.formalpolarization import main
    atoms.write('structure.json')
    main()


abn = 2.51
BN = Atoms(
    "BN",
    scaled_positions=[[0, 0, 0], [1 / 3, 2 / 3, 0]],
    cell=[
        [abn, 0.0, 0.0],
        [-0.5 * abn, np.sqrt(3) / 2 * abn, 0],
        [0.0, 0.0, 15.0],
    ],
    pbc=[True, True, False],
)

Ag_chain = Atoms(
    "Ag",
    scaled_positions=[[0, 0, 0]],
    cell=[
        [15.0, 0.0, 0.0],
        [0.0, 15.0, 0.0],
        [0.0, 0.0, 2],
    ],
    pbc=[False, False, True],
)

bad_atoms = [BN, Ag_chain]


@pytest.mark.ci
@pytest.mark.parametrize("atoms", bad_atoms)
def test_formalpolarization_test_atoms_too_close_to_boundary(
        separate_folder, mockgpaw, atoms):
    from asr.formalpolarization import AtomsTooCloseToBoundary, main
    atoms.write("structure.json")

    with pytest.raises(AtomsTooCloseToBoundary):
        main()
