"""Read scientific input files, execute the stated method, and report observables."""
from pathlib import Path
import numpy as np
from catalysis.teaching_io import arguments, controls, table, column, write_table, record, summary, read_xyz, atom_string
args = arguments(Path(__file__).parent)
c = controls(args.input)
from catalysis.thermo import surface_phase
from ase.io import read
states=[]
for r in table(args.input/'states.csv'):
    n=int(r['adsorbates']);atoms=read(args.input/(r['name']+'.POSCAR'),format='vasp')
    if atoms.get_chemical_symbols().count('H')!=n:raise ValueError('Composition differs from state table')
    states.append({'name':r['name'],'energy_eV':float(r['energy_eV']),'adsorbates':n})
result=surface_phase(states,np.linspace(*c['mu_grid_eV']))
result['model']='Synthetic state energies for grand-potential algebra; POSCAR illustrates composition, not a DFT energy source.'
write_table(args.output/'phase.csv',['mu_eV',*[s['name']+'_Omega_eV' for s in states],'stable_state'],
    zip(result['mu_eV'],*result['grand_potential_eV'],result['stable_state']))

from catalysis.teaching_io import export_tables
export_tables(args.output, result)
record(args, result, '\n'.join(summary(result)) + '\nTables and arrays are saved alongside this report.')
