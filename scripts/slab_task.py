"""Run one native POSCAR/GPAW case, optionally selected by a Slurm array."""
import argparse
import os
from pathlib import Path
from catalysis.native_dft import calculate_case
from catalysis.teaching_io import table,write_table
p=argparse.ArgumentParser()
p.add_argument('--input',type=Path,required=True,help='Project input directory containing cases.csv')
p.add_argument('--output',type=Path,required=True)
p.add_argument('--index',type=int,default=int(os.environ.get('SLURM_ARRAY_TASK_ID',0)))
a=p.parse_args();case=table(a.input/'cases.csv')[a.index]
folder=a.output/case['scenario'];folder.mkdir(parents=True,exist_ok=True)
rows=[{'scenario':case['scenario'],**r} for r in calculate_case(a.input/case['directory'],folder)]
write_table(folder/'energies.csv',list(rows[0]),[list(r.values()) for r in rows])
print(folder/'energies.csv')
