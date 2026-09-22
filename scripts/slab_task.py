"""Run one independent convergence task (optionally through a Slurm job array).

After all tasks finish, run the normal project CLI with the same output directory;
it validates and reuses the completed tasks and writes the aggregate result.
"""
import argparse
import json
import os
from pathlib import Path
from catalysis.surfaces import cached_adsorption,slab_tasks
p=argparse.ArgumentParser()
p.add_argument('--input',type=Path,required=True)
p.add_argument('--output',type=Path,required=True)
p.add_argument('--index',type=int,default=int(os.environ.get('SLURM_ARRAY_TASK_ID',0)))
a=p.parse_args()
config=json.loads(a.input.read_text())['parameters']
tasks=list(slab_tasks(config))
name,settings=tasks[a.index]
result=cached_adsorption(settings,a.output/name)
print(json.dumps({'task':name,'result':result},indent=2),flush=True)
