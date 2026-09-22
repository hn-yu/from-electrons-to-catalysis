"""Project entry points. Never overwrite checked-in expected output by default."""
import argparse
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import subprocess


def run_project(project):
    project = Path(project).resolve()
    parser = argparse.ArgumentParser(description=project.name)
    parser.add_argument('--input',type=Path,default=project/'input'/'example.json')
    parser.add_argument('--output',type=Path,default=Path('runs')/project.name)
    args = parser.parse_args()
    execute(project,args.input,args.output)


def execute(project,input_path,output):
    from .experiments import EXPERIMENTS
    raw = Path(input_path).read_bytes(); config = json.loads(raw)
    output = Path(output); output.mkdir(parents=True,exist_ok=True)
    result = EXPERIMENTS[config['experiment']](config['parameters'],output)
    versions = {'python':platform.python_version()}
    for package in ['numpy','scipy','ase','pyscf','gpaw']:
        try:
            versions[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            pass
    git = subprocess.run(['git','rev-parse','HEAD'],capture_output=True,text=True,cwd=project)
    payload = {'project':str(Path(project).name), 'input':config, 'input_sha256':hashlib.sha256(raw).hexdigest(),
               'versions':versions, 'source_revision':git.stdout.strip() if git.returncode == 0 else None,
               'slurm_job_id':os.environ.get('SLURM_JOB_ID'), 'result':result}
    target = output/'result.json'
    target.write_text(json.dumps(payload,indent=2,allow_nan=False)+'\n')
    print(target,flush=True)
    return payload
