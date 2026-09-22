"""Read scientific input files, execute the stated method, and report observables."""
from pathlib import Path
import numpy as np
from catalysis.teaching_io import arguments, controls, table, column, write_table, record, summary, read_xyz, atom_string
args = arguments(Path(__file__).parent)
c = controls(args.input)
from catalysis.experiments import mep_fes
from scipy.integrate import quad
from catalysis.units import kbt
c['temperatures_K']=column(args.input/'temperatures.csv','T_K');result=mep_fes(c,args.output)
x=np.array(result['x']);mep=np.array(result['MEP_eV'])
for r in result['finite_temperature']:
    kt=float(kbt(r['T_K']))
    # Integrate out y independently; potential U=MEP(x)+(1+x²)y².
    numerical=np.array([-kt*np.log(quad(lambda y:np.exp(-(1+v*v)*y*y/kt),-np.inf,np.inf)[0])+e for v,e in zip(x,mep)])
    numerical-=numerical.min();r['quadrature_max_error_eV']=float(np.max(abs(numerical-r['F_eV'])))
    write_table(args.output/f'F-{r["T_K"]:g}K.csv',['x_model','MEP_eV','F_analytic_eV','F_quadrature_eV'],zip(x,mep,r['F_eV'],numerical))

from catalysis.teaching_io import export_tables
export_tables(args.output, result)
record(args, result, '\n'.join(summary(result)) + '\nTables and arrays are saved alongside this report.')
