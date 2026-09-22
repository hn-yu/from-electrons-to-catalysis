"""Scientific text inputs and readable output; no experiment dispatcher."""
import argparse
import csv
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import subprocess
import numpy as np
try:
    import tomllib
except ImportError:
    import tomli as tomllib


def arguments(project):
    project=Path(project).resolve()
    parser=argparse.ArgumentParser(description=project.name)
    parser.add_argument('--input',type=Path,default=project/'input',help='Directory containing scientific input files')
    parser.add_argument('--output',type=Path,default=Path('runs')/project.name)
    parser.add_argument('--calculate',action='store_true',help='Run new electronic-structure jobs where a project supports them')
    args=parser.parse_args()
    args.project=project
    args.source_revision=subprocess.run(['git','rev-parse','HEAD'],cwd=project,text=True,capture_output=True).stdout.strip()
    args.source_files_sha256={str(p.relative_to(project.parents[1])):hashlib.sha256(p.read_bytes()).hexdigest() for base in [project,project.parents[1]/'src'] for p in base.rglob('*.py') if '__pycache__' not in p.parts}
    if not args.input.is_dir():
        parser.error('--input must be a directory containing coordinates/tables and control.toml')
    args.output.mkdir(parents=True,exist_ok=True)
    return args


def controls(directory):
    path=Path(directory)/'control.toml'
    return tomllib.loads(path.read_text()) if path.exists() else {}


def table(path):
    with Path(path).open(newline='') as stream:
        return list(csv.DictReader(stream))


def column(path,name):
    return [float(row[name]) for row in table(path)]


def write_table(path,headers,rows):
    with Path(path).open('w',newline='') as stream:
        writer=csv.writer(stream);writer.writerow(headers);writer.writerows(rows)


def read_xyz(path):
    from ase.io import read
    atoms=read(str(path))
    if not np.isfinite(atoms.positions).all():
        raise ValueError('Nonfinite atomic coordinate')
    return atoms


def atom_string(atoms):
    return '; '.join(f'{symbol} {x:.14g} {y:.14g} {z:.14g}' for symbol,(x,y,z) in zip(atoms.get_chemical_symbols(),atoms.positions))


def record(args,result,report):
    """Human-readable report is primary; JSON is a machine-readable audit companion."""
    versions={}
    for name in ['numpy','scipy','ase','pyscf','gpaw','pymbar','cantera']:
        try:versions[name]=importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:pass
    files={str(p.relative_to(args.input)):hashlib.sha256(p.read_bytes()).hexdigest()
           for p in sorted(args.input.rglob('*')) if p.is_file() and '__pycache__' not in p.parts}
    payload={'project':args.project.name,'input_files_sha256':files,'versions':versions,
             'source_revision':args.source_revision,'source_files_sha256':args.source_files_sha256,'slurm_job_id':os.environ.get('SLURM_JOB_ID'),'result':result}
    (args.output/'result.json').write_text(json.dumps(payload,indent=2,allow_nan=False)+'\n')
    (args.output/'report.txt').write_text(report.rstrip()+'\n')
    print(report,flush=True)
    return payload


def summary(value,prefix=''):
    """Short named observables, not a dump of wavefunctions or nested configuration."""
    lines=[]
    for key,item in value.items():
        name=f'{prefix}{key}'
        if isinstance(item,dict):lines.extend(summary(item,name+'.'))
        elif isinstance(item,list) and len(item)<=40 and all(isinstance(r,dict) for r in item):
            for i,row in enumerate(item):lines.extend(summary(row,f'{name}[{i}].'))
        elif isinstance(item,(float,int,str,bool)):lines.append(f'{name}: {item}')
        elif isinstance(item,list) and len(item)<=8 and all(isinstance(x,(float,int,str)) for x in item):
            lines.append(f'{name}: '+', '.join(map(str,item)))
    return lines


def export_tables(folder, result, prefix=''):
    """Expose numeric arrays and row records without requiring JSON inspection."""
    folder=Path(folder)
    for key,value in result.items():
        name=(prefix+key).replace('/','_')
        if isinstance(value,dict):export_tables(folder,value,name+'-')
        elif isinstance(value,list) and value:
            if all(isinstance(r,dict) for r in value):
                keys=list(dict.fromkeys(k for r in value for k,v in r.items() if isinstance(v,(float,int,str,bool))))
                if keys:write_table(folder/(name+'.csv'),keys,[[r.get(k,'') for k in keys] for r in value])
                for i,r in enumerate(value):export_tables(folder,{k:v for k,v in r.items() if isinstance(v,(dict,list))},f'{name}-{i}-')
            else:
                try:array=np.asarray(value,dtype=float)
                except (ValueError,TypeError):continue
                if array.ndim==2:
                    headers=result.get('columns',[f'column_{i}' for i in range(array.shape[1])])
                    if len(headers)!=array.shape[1]:headers=[f'column_{i}' for i in range(array.shape[1])]
                    write_table(folder/(name+'.csv'),headers,array)
                elif array.ndim==1:np.savetxt(folder/(name+'.dat'),array,header=name)
