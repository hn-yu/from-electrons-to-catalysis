"""Read scientific input files, execute the stated method, and report observables."""
from pathlib import Path
import numpy as np
from catalysis.teaching_io import arguments, controls, table, column, write_table, record, summary, read_xyz, atom_string
args = arguments(Path(__file__).parent)
c = controls(args.input)
from catalysis.potentials import Morse, finite_force
atoms=read_xyz(args.input/c['geometry']);r=atoms.get_distance(0,1);p=Morse()
rows=[[float(h),abs(float(finite_force(p,r,h))-float(p.force(r)))] for h in np.logspace(*c['log10_step_range'])]
result={'r_A':r,'analytic_force_eV_A':float(p.force(r)),'columns':['h_A','absolute_error_eV_A'],'scan':rows,
        'best_step_A':rows[int(np.argmin(np.array(rows)[:,1]))][0]}

from catalysis.teaching_io import export_tables
export_tables(args.output, result)
record(args, result, '\n'.join(summary(result)) + '\nTables and arrays are saved alongside this report.')
