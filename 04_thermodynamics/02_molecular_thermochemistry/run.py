"""Read scientific input files, execute the stated method, and report observables."""
from pathlib import Path
import numpy as np
from catalysis.teaching_io import arguments, controls, table, column, write_table, record, summary, read_xyz, atom_string
args = arguments(Path(__file__).parent)
c = controls(args.input)
from catalysis.quantum import molecular_thermo
from ase import Atoms
from ase.io import write
c['molecules']=[]
for r in table(args.input/'molecules.csv'):
    atoms=read_xyz(args.input/r['geometry'])
    c['molecules'].append({'name':r['molecule'],'symbols':atoms.get_chemical_symbols(),'positions_A':atoms.positions.tolist(),
                           'symmetry':int(r['symmetry']),'linear':r['linear'].lower() in ['true','1'],'spin':float(r['spin'])})
result=molecular_thermo(c)
for row,item in zip(result['results'],c['molecules']):
    write(args.output/(row['molecule']+'-optimized.xyz'),Atoms(item['symbols'],positions=row['positions_A']))

from catalysis.teaching_io import export_tables
export_tables(args.output, result)
record(args, result, '\n'.join(summary(result)) + '\nTables and arrays are saved alongside this report.')
