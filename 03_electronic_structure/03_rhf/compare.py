"""Recompute PySCF RHF from XYZ and check cached integrals against those coordinates."""
from pathlib import Path
import argparse
import numpy as np
from pyscf import gto,scf
from catalysis.integral_files import load_integrals
from catalysis.electronic import rhf_from_integrals
from catalysis.teaching_io import read_xyz,atom_string,table

p=argparse.ArgumentParser();p.add_argument('--input',type=Path,default=Path(__file__).parent/'input');a=p.parse_args()
for case in table(a.input/'cases.csv'):
    geometry=a.input/case['geometry']
    if int(case['spin'])!=0:raise ValueError('This project implements closed-shell RHF only')
    mol=gto.M(atom=atom_string(read_xyz(geometry)),basis=case['basis'],charge=int(case['charge']),spin=int(case['spin']),verbose=0)
    s,h,eri,n,enuc=load_integrals(geometry.parent)
    np.testing.assert_allclose(s,mol.intor('int1e_ovlp'),atol=1e-12)
    np.testing.assert_allclose(h,mol.intor('int1e_kin')+mol.intor('int1e_nuc'),atol=1e-12)
    np.testing.assert_allclose(eri,mol.intor('int2e'),atol=1e-12)
    assert n==mol.nelectron and abs(enuc-mol.energy_nuc())<1e-10
    ref=scf.RHF(mol).run(conv_tol=1e-11)
    own=rhf_from_integrals(s,h,eri,n,enuc)
    assert ref.converged and abs(own['energy_Hartree']-ref.e_tot)<1e-8
    np.testing.assert_allclose(own['matrices']['D_final'],ref.make_rdm1(),atol=2e-6)
    np.testing.assert_allclose(own['matrices']['F_final'],ref.get_fock(),atol=2e-6)
    print(case['case'],'geometry/integrals/electron count/energy agree')
