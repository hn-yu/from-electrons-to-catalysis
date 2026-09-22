"""Execute each project's public native-file entry point. Submit with Slurm on HPC."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
root=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--tiers',nargs='+',default=['core'])
parser.add_argument('--output-root',type=Path,default=root/'runs'/'all')
parser.add_argument('--exclude',nargs='*',default=[])
args=parser.parse_args()
for project in json.loads((root/'projects.json').read_text()):
    if project['tier'] in args.tiers and project['experiment'] not in args.exclude:
        folder=root/project['path']
        print('Running '+project['path'],flush=True)
        subprocess.run([sys.executable,str(folder/'run.py'),'--input',str(folder/'input'),
                        '--output',str(args.output_root/project['path'])],check=True)
