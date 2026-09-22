"""Read scientific input files, execute the stated method, and report observables."""
from pathlib import Path
import numpy as np
from catalysis.teaching_io import arguments, controls, table, column, write_table, record, summary, read_xyz, atom_string
args = arguments(Path(__file__).parent)
c = controls(args.input)
from scipy.optimize import minimize as scipy_minimize
from catalysis.kinetics import minimize
from catalysis.potentials import Morse,MullerBrown
rows=[]
for name,p,starts in [('Morse',Morse(),np.loadtxt(args.input/'morse_starts.dat',ndmin=1)[:,None]),
                       ('MullerBrown',MullerBrown(),np.loadtxt(args.input/'mb_starts.dat',ndmin=2))]:
    for start in starts:
        own=minimize(p,start);ref=scipy_minimize(p.energy,start,jac=lambda x:-p.force(x),method='BFGS',options={'gtol':1e-6})
        if np.linalg.norm(p.force(ref.x))>2e-6: raise RuntimeError('SciPy optimizer did not reach stationarity')
        rows.append({'potential':name,'start':start.tolist(),'own':own,'SciPy_energy':float(ref.fun),
                     'SciPy_x':ref.x.tolist(),'energy_difference':own['energy']-float(ref.fun)})
result={'minima':rows}

from catalysis.teaching_io import export_tables
export_tables(args.output, result)
record(args, result, '\n'.join(summary(result)) + '\nTables and arrays are saved alongside this report.')
