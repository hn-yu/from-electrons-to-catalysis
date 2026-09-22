"""Read scientific input files, execute the stated method, and report observables."""
from pathlib import Path
import numpy as np
from catalysis.teaching_io import arguments, controls, table, column, write_table, record, summary, read_xyz, atom_string
args = arguments(Path(__file__).parent)
c = controls(args.input)
from scipy.linalg import eigh_tridiagonal
result={}
for name in ['box','harmonic','finite_well','double_well']:
    data=np.loadtxt(args.input/f'{name}.dat');x,v=data.T;dx=x[1]-x[0]
    if not np.allclose(np.diff(x),dx): raise ValueError('Uniform interior grid required')
    # Hand assemble -1/2 d²/dx² + V, with Dirichlet walls one grid step outside.
    diagonal=1/dx**2+v;off=np.full(len(x)-1,-.5/dx**2)
    e,psi=eigh_tridiagonal(diagonal,off,select='i',select_range=(0,c['states']-1));psi/=np.sqrt(dx)
    write_table(args.output/f'{name}-wavefunctions.csv',['x_bohr','V_Hartree',*[f'psi_{i}' for i in range(c['states'])]],np.column_stack([x,v,psi]))
    analytic=(np.arange(1,c['states']+1)**2*np.pi**2/(2*((len(x)+1)*dx)**2) if name=='box' else np.arange(c['states'])+.5 if name=='harmonic' else None)
    result[name]={'energies_Hartree':e.tolist(),'normalization':(np.sum(psi**2,axis=0)*dx).tolist()}
    if analytic is not None: result[name]['analytic_error_Hartree']=(e-analytic).tolist()

from catalysis.teaching_io import export_tables
export_tables(args.output, result)
record(args, result, '\n'.join(summary(result)) + '\nTables and arrays are saved alongside this report.')
