"""Read scientific input files, execute the stated method, and report observables."""
from pathlib import Path
import numpy as np
from catalysis.teaching_io import arguments, controls, table, column, write_table, record, summary, read_xyz, atom_string
args = arguments(Path(__file__).parent)
c = controls(args.input)
from catalysis.quantum import hf_failures
geometries=[read_xyz(args.input/r['file']) for r in table(args.input/'geometries.csv')]
c['geometries']=[atom_string(a) for a in geometries]
c['bond_lengths_A']=[a.get_distance(0,1) for a in geometries]
if (args.input/'O2.xyz').exists():c['oxygen_geometry']=atom_string(read_xyz(args.input/'O2.xyz'))
result=hf_failures(c)

from catalysis.teaching_io import export_tables
export_tables(args.output, result)
record(args, result, '\n'.join(summary(result)) + '\nTables and arrays are saved alongside this report.')
