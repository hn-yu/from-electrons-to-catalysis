"""Fit supplied PBE E(V) data, or calculate a new curve from Al.cif with GPAW."""
from pathlib import Path
import numpy as np
from ase.io import read
from ase.eos import EquationOfState
from ase.units import GPa
from catalysis.surfaces import calculator
from catalysis.teaching_io import arguments,controls,table,column,write_table,record,summary,export_tables
args=arguments(Path(__file__).parent);c=controls(args.input)
if c.get('backend')!='gpaw':raise ValueError('The native PBE project requires backend=gpaw')
if args.calculate:
    initial=read(args.input/'Al.cif');a_initial=(4*initial.get_volume()/len(initial))**(1/3)
    rows=[]
    for a in column(args.input/'lattice_scan.csv','a_A'):
        atoms=initial.copy();atoms.set_cell(initial.cell*a/a_initial,scale_atoms=True)
        atoms.calc=calculator(c,args.output/f'gpaw-a{a:g}.txt')
        rows.append({'scenario':'baseline','a_A':a,'volume_A3_atom':atoms.get_volume()/len(atoms),'energy_eV_atom':atoms.get_potential_energy()/len(atoms)})
    write_table(args.output/'eos.csv',list(rows[0]),[list(r.values()) for r in rows])
else:rows=table(args.input/'eos.csv')
fits={}
for scenario in dict.fromkeys(r['scenario'] for r in rows):
    selected=[r for r in rows if r['scenario']==scenario]
    v=np.array([float(r['volume_A3_atom']) for r in selected]);e=np.array([float(r['energy_eV_atom']) for r in selected])
    v0,e0,b=EquationOfState(v,e,eos='birchmurnaghan').fit()
    if not v.min()<v0<v.max():raise RuntimeError('EOS minimum lies outside sampled volumes')
    fits[scenario]={'a0_A':float((4*v0)**(1/3)),'bulk_modulus_GPa':float(b/GPa),'minimum_energy_eV_atom':float(e0)}
result={'backend':'gpaw',**fits['baseline'],'convergence_fits':fits,
        'execution':'New GPAW calculation' if args.calculate else 'Fit of archived GPAW/PBE results; raw example log: output/gpaw-Al-a4.06.txt'}
export_tables(args.output,result);record(args,result,'\n'.join(summary(result)))
