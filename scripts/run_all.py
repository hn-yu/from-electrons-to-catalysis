"""Execute examples by dependency tier. Submit this script through Slurm on a cluster."""
import argparse
import json
from pathlib import Path
from catalysis.cli import execute

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--tiers',nargs='+',default=['core'])
parser.add_argument('--output-root',type=Path,default=root/'runs'/'all')
args = parser.parse_args()
for project in json.loads((root/'projects.json').read_text()):
    if project['tier'] in args.tiers:
        folder = root/project['path']
        print('Running '+project['path'],flush=True)
        execute(folder,folder/'input'/'example.json',args.output_root/project['path'])
