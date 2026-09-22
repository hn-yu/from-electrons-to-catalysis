"""Check native input/output provenance and local documentation links."""
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import unquote
root=Path(__file__).resolve().parents[1]
projects=json.loads((root/'projects.json').read_text())
for project in projects:
    folder=root/project['path']
    for name in ['README.md','input/README.md','output/README.md','hints/README.md','hints/hint1.md','hints/hint2.md','hints/hint3.md']:
        assert (folder/name).is_file(),folder/name
    assert not list((folder/'input').rglob('*.json')),f'Active JSON input: {folder}'
    if project['tier']=='written':
        for name in ['input/questions.md','output/answer.md']:assert (folder/name).exists(),folder/name
    else:
        for name in ['run.py','output/result.json','output/report.txt']:assert (folder/name).exists(),folder/name
        data=json.loads((folder/'output/result.json').read_text())
        actual={str(f.relative_to(folder/'input')):hashlib.sha256(f.read_bytes()).hexdigest()
                for f in (folder/'input').rglob('*') if f.is_file() and '__pycache__' not in f.parts}
        assert data['input_files_sha256']==actual,f'Input changed since output generation: {folder}'
        for name,digest in data['source_files_sha256'].items():
            assert hashlib.sha256((root/name).read_bytes()).hexdigest()==digest,f'Source changed since output generation: {name}'
# Historical archives retain their original text; active guides must have valid local links.
active=[root/'README.md',root/'INSTALL.md',root/'docs/IMPLEMENTATION_BOUNDARIES.md']
active.extend(sorted({root/Path(project['path']).parent/'README.md' for project in projects}))
for project in projects:
    folder=root/project['path']
    active.extend([folder/'README.md',folder/'input/README.md',folder/'output/README.md',*sorted((folder/'hints').glob('*.md'))])
errors=[]
for path in active:
    for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)',path.read_text()):
        if target.startswith(('http:','https:','mailto:','#')):continue
        target=unquote(target.split('#')[0])
        if not (path.parent/target).exists():errors.append(f'{path.relative_to(root)} -> {target}')
assert not errors,'Broken active links:\n'+'\n'.join(errors)
print(f'{len(projects)} project layouts, native input hashes, source hashes and active local links verified')
