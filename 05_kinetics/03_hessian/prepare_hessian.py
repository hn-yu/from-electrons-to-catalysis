"""Generate a real molecular Cartesian Hessian using PySCF; run.py owns mass weighting."""
from pathlib import Path
import numpy as np
from pyscf import gto,scf
from scipy.optimize import minimize
from ase.io import write
from catalysis.teaching_io import read_xyz,atom_string

import argparse
p=argparse.ArgumentParser();p.add_argument('--input',type=Path,default=Path(__file__).parent/'input')
folder=p.parse_args().input
atoms=read_xyz(folder/'H2O.xyz')
def objective(flat):
    trial=atoms.copy();trial.positions=flat.reshape(-1,3)
    mol=gto.M(atom=atom_string(trial),basis='sto-3g',verbose=0)
    mf=scf.RHF(mol).run(conv_tol=1e-12)
    if not mf.converged:raise RuntimeError('SCF failed')
    return mf.e_tot,mf.nuc_grad_method().kernel().ravel()/0.529177210903
opt=minimize(objective,atoms.positions.ravel(),jac=True,method='BFGS',options={'gtol':1e-6})
if np.max(abs(opt.jac))>3e-6:raise RuntimeError('Geometry not stationary')
atoms.positions=opt.x.reshape(-1,3);write(folder/'H2O_optimized.xyz',atoms,format='xyz')
mol=gto.M(atom=atom_string(atoms),basis='sto-3g',verbose=0);mf=scf.RHF(mol).run(conv_tol=1e-12)
raw=mf.Hessian().kernel()  # PySCF order: atom, atom, Cartesian, Cartesian.
hessian=raw.transpose(0,2,1,3).reshape(3*len(atoms),3*len(atoms))
np.savetxt(folder/'hessian.dat',hessian,fmt='% .14e',header='Cartesian Hessian, Hartree/bohr^2; x1 y1 z1 x2 y2 z2 ...')
np.savetxt(folder/'masses.dat',atoms.get_masses(),header='atomic masses, u')
print('Wrote optimized XYZ and',hessian.shape,'PySCF Cartesian Hessian')
