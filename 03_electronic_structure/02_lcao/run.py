"""Read scientific input files, execute the stated method, and report observables."""
from pathlib import Path
import numpy as np
from catalysis.teaching_io import arguments, controls, table, column, write_table, record, summary, read_xyz, atom_string
args = arguments(Path(__file__).parent)
c = controls(args.input)
from scipy.linalg import eigh
h=np.loadtxt(args.input/'hamiltonian.dat');s=np.loadtxt(args.input/'overlap.dat')
w,u=np.linalg.eigh(s)
if w.min()<=1e-10: raise ValueError('S must be positive definite')
x=(u/np.sqrt(w))@u.T
energy,v=np.linalg.eigh(x.T@h@x);coeff=x@v
reference,_=eigh(h,s)
for name,matrix in [('X',x),('coefficients',coeff),('C_transpose_S_C',coeff.T@s@coeff)]:np.savetxt(args.output/f'{name}.dat',matrix)
result={'energies_Hartree':energy.tolist(),'SciPy_energies_Hartree':reference.tolist(),
        'max_reference_error':float(np.max(abs(energy-reference))), 'generalized_residual':float(np.linalg.norm(h@coeff-s@coeff@np.diag(energy)))}

from catalysis.teaching_io import export_tables
export_tables(args.output, result)
record(args, result, '\n'.join(summary(result)) + '\nTables and arrays are saved alongside this report.')
