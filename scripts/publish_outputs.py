"""Copy a reviewed run tree into its project output directory.

This is an explicit maintainer operation, separate from ordinary project runners.
Only portable result artifacts are included; wavefunction caches are excluded.
"""
import argparse
import json
import shutil
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument('--source',type=Path,required=True)
p.add_argument('--destination',type=Path,required=True)
a=p.parse_args()
if not (a.source/'result.json').is_file():
    raise SystemExit('Source has no completed result.json')
json.loads((a.source/'result.json').read_text())
for source in a.source.rglob('*'):
    if source.is_file() and source.suffix in {'.json','.csv','.extxyz','.svg'}:
        destination=a.destination/source.relative_to(a.source)
        if source.name=='completed.json':
            # Archive task provenance without making the reference tree a live cache.
            destination=destination.with_name('task_result.json')
        destination.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(source,destination)
