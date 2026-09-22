import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]

def test_project_entrypoint_from_other_working_directory(tmp_path):
    script=ROOT/'02_bringup/01_units/run.py'
    output=tmp_path/'result'
    run=subprocess.run([sys.executable,str(script),'--output',str(output)],cwd=tmp_path,capture_output=True,text=True)
    assert run.returncode==0,run.stderr
    data=json.loads((output/'result.json').read_text())
    assert data['result']['thermal_scales'][0]['kBT_eV']>0
    assert data['input_files_sha256']['conversions.csv'] and data['source_files_sha256']
    assert (output/'report.txt').exists()
    assert not (tmp_path/'output').exists()
