"""Read scientific input files, execute the stated method, and report observables."""
from pathlib import Path
import numpy as np
from catalysis.teaching_io import arguments, controls, table, column, write_table, record, summary, read_xyz, atom_string
args = arguments(Path(__file__).parent)
c = controls(args.input)
from catalysis.thermo import partition, oscillator
levels=table(args.input/'levels.csv');energy=[float(r['energy_eV']) for r in levels];deg=[float(r['degeneracy']) for r in levels]
result={'two_level':[{'T_K':t,**partition(energy,t,deg)} for t in column(args.input/'temperatures.csv','T_K')],
        'oscillator':[{'T_K':t,**oscillator(c['quantum_eV'],t)} for t in column(args.input/'temperatures.csv','T_K')]}

from catalysis.teaching_io import export_tables
export_tables(args.output, result)
record(args, result, '\n'.join(summary(result)) + '\nTables and arrays are saved alongside this report.')
