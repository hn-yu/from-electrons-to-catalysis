"""Small integration check: GPAW receives the actual supplied POSCAR coordinates."""
from pathlib import Path
import numpy as np
from ase.io import read,write
from catalysis.surfaces import calculator
import tomllib
folder=Path('07_real_system/02_real_dft/input/baseline')
output=Path('runs/native-gpaw-check');output.mkdir(exist_ok=True)
config=tomllib.loads((folder/'calculator.toml').read_text())
atoms=read(folder/'fcc.POSCAR',format='vasp')
assert len(atoms)==4 and atoms.get_chemical_symbols().count('H')==1
positions=atoms.positions.copy();cell=atoms.cell.copy()
atoms.calc=calculator(config,output/'fcc-singlepoint-gpaw.txt')
energy=atoms.get_potential_energy();forces=atoms.get_forces()
assert np.isfinite(energy) and np.isfinite(forces).all()
np.testing.assert_array_equal(atoms.positions,positions)
np.testing.assert_array_equal(atoms.cell,cell)
write(output/'fcc-singlepoint.extxyz',atoms)
(output/'report.txt').write_text(f'GPAW/PBE single point from baseline/fcc.POSCAR\nE_extrapolated_eV = {energy:.12f}\nmax_unconstrained_force_eV_A = {np.linalg.norm(forces,axis=1).max():.8f}\nThis unrelaxed single point checks native I/O, not adsorption convergence.\n')
print((output/'report.txt').read_text())
