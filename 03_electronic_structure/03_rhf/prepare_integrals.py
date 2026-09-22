"""Use PySCF as an AO integral engine; the student SCF reads the emitted text files."""
from pathlib import Path
import argparse
from pyscf import gto,scf
from catalysis.teaching_io import table,read_xyz,atom_string
from catalysis.integral_files import export_integrals


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--input',type=Path,default=Path(__file__).parent/'input')
    args=p.parse_args()
    for case in table(args.input/'cases.csv'):
        geometry=args.input/case['geometry']
        if int(case['spin'])!=0:raise ValueError('Closed-shell RHF requires spin=0')
        mol=gto.M(atom=atom_string(read_xyz(geometry)),basis=case['basis'],
                  charge=int(case['charge']),spin=int(case['spin']),verbose=0)
        export_integrals(mol,geometry.parent)
        # An independent library run supplies a reference, never the student's iteration.
        mf=scf.RHF(mol).run(conv_tol=1e-11)
        if not mf.converged:raise RuntimeError('Reference RHF failed')
        (geometry.parent/'pyscf_reference.dat').write_text(f'{mf.e_tot:.16f}\n')
        print(case['case'],mol.nao_nr(),mf.e_tot,flush=True)

if __name__=='__main__':main()
