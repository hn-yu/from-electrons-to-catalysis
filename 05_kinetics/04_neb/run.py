"""Read scientific input files, execute the stated method, and report observables."""
from pathlib import Path
import numpy as np
from catalysis.teaching_io import arguments, controls, table, column, write_table, record, summary, read_xyz, atom_string
args = arguments(Path(__file__).parent)
c = controls(args.input)
from catalysis.experiments import neb,atom_diffusion
c['endpoints']=np.loadtxt(args.input/'endpoints.dat').tolist()
result=neb(c,args.output)
write_table(args.output/'own-band.csv',['x_model','y_model','E_eV'],np.column_stack([result['own']['path'],result['own']['energies_eV']]))
atomic=args.output/'atomic';atomic.mkdir(exist_ok=True)
result['atomic']=atom_diffusion({'images':9,'endpoint_files':[str(args.input/'fcc.extxyz'),str(args.input/'hcp.extxyz')]},atomic)

from catalysis.teaching_io import export_tables
export_tables(args.output, result)
record(args, result, '\n'.join(summary(result)) + '\nTables and arrays are saved alongside this report.')
