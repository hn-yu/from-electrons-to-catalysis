"""Validate that every course project has reviewable inputs, outputs and hints."""
import hashlib
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
projects=json.loads((root/'projects.json').read_text())
for project in projects:
    folder=root/project['path']
    for name in ['README.md','hints/README.md']:
        assert (folder/name).is_file(),folder/name
    if project['tier']=='written':
        for name in ['input/questions.md','output/answer.md']:
            assert (folder/name).is_file(),folder/name
    else:
        for name in ['run.py','input/example.json','output/result.json','output/analysis.md']:
            assert (folder/name).is_file(),folder/name
        raw=(folder/'input/example.json').read_bytes()
        output=json.loads((folder/'output/result.json').read_text())
        assert output['input']==json.loads(raw),folder
        assert output['input_sha256']==hashlib.sha256(raw).hexdigest(),folder
print(f'{len(projects)} complete projects: inputs, outputs, README, hints and hashes verified')
