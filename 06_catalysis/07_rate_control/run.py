"""Read scientific input files, execute the stated method, and report observables."""
from pathlib import Path
import numpy as np
from catalysis.teaching_io import arguments, controls, table, column, write_table, record, summary, read_xyz, atom_string
args = arguments(Path(__file__).parent)
c = controls(args.input)
from catalysis.experiments import rate_control
from catalysis.cantera_reference import model_from_tables,solve,rate_control as ct_control
from catalysis.network import steady_state
c['model']=model_from_tables(args.input)
for key,file,col in [('temperatures_K','temperatures.csv','T_K'),('pressures_bar','pressures.csv','p_bar')]:
    if (args.input/file).exists():c[key]=column(args.input/file,col)
result=rate_control(c,args.output)
pa=c.get('pA_bar',1.);pb=c.get('pB_bar',.01);t=c['temperature_K']
own=steady_state(c['model'],t,pa,pb);reference=solve(args.input/'mechanism.yaml',t,pa,pb)
result['own_steady_state']=own;result['Cantera']=reference
result['coverage_max_error']=float(np.max(abs(np.array(own['coverages'])-reference['coverages'])))
result['TOF_relative_error']=abs(own['TOF_s^-1']/reference['TOF_s^-1']-1)
if 'rate_control'=='rate_control':result['Cantera_degree_of_rate_control']=ct_control(args.input/'mechanism.yaml',t)
if 'sweep' in result:
    for row in result['sweep']:
        ref=solve(args.input/'mechanism.yaml',row['T_K'],row['pA_bar'],pb)
        row['Cantera_TOF_s^-1']=ref['TOF_s^-1'];row['relative_error']=abs(row['TOF_s^-1']/ref['TOF_s^-1']-1)

from catalysis.teaching_io import export_tables
export_tables(args.output, result)
record(args, result, '\n'.join(summary(result)) + '\nTables and arrays are saved alongside this report.')
