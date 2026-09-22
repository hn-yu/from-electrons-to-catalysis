"""Read indexed AO files → handwritten RHF/DIIS → compare PySCF reference.

This program never invokes PySCF's SCF inside the handwritten loop. Regenerate
integrals with prepare_integrals.py when changing geometry/basis/charge.
"""
from pathlib import Path
import numpy as np
from catalysis.electronic import rhf_from_integrals
from catalysis.integral_files import load_integrals
from catalysis.teaching_io import arguments,controls,table,record,write_table


def main():
    args=arguments(Path(__file__).parent)
    config=controls(args.input)
    results={};lines=['Restricted Hartree-Fock: indexed AO input, spin-summed D=2 Cocc Cocc^T','']
    for case in table(args.input/'cases.csv'):
        folder=(args.input/case['geometry']).parent
        s,h,eri,nelectron,enuc=load_integrals(folder)
        calculation=rhf_from_integrals(s,h,eri,nelectron,enuc,**config)
        reference=float(np.loadtxt(folder/'pyscf_reference.dat'))
        calculation['reference_Hartree']=reference
        calculation['error_Hartree']=calculation['energy_Hartree']-reference
        destination=args.output/folder.name;destination.mkdir(exist_ok=True)
        for name,matrix in calculation['matrices'].items():
            np.savetxt(destination/(name+'.dat'),matrix,fmt='% .12f',header=name)
        write_table(destination/'iterations.csv',
                    ['iteration','E_total_Hartree','density_change_Frobenius','commutator_norm'],calculation['history'])
        lines += [f'CASE {case["case"]}; {case["basis"]}; nAO={len(s)}; Ne={nelectron}',
                  f'Enuc = {enuc:.12f} Hartree',
                  f'own   = {calculation["energy_Hartree"]:.12f} Hartree',
                  f'PySCF = {reference:.12f} Hartree',
                  f'difference = {calculation["error_Hartree"]:.3e} Hartree',
                  f'Tr(D S) = {calculation["electrons"]:.12f}',
                  'iteration E_total_Hartree ||deltaD|| ||FDS-SDF||']
        lines += ['%3d % .12f %.5e %.5e'%tuple(row) for row in calculation['history']]
        lines += ['S =',np.array2string(s,precision=7),'X =',np.array2string(np.array(calculation['matrices']['X']),precision=7),'']
        results[case['case']]=calculation
    record(args,results,'\n'.join(lines))

if __name__=='__main__':main()
