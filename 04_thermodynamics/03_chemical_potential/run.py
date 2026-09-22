"""Read scientific input files, execute the stated method, and report observables."""
from pathlib import Path
import numpy as np
from catalysis.teaching_io import arguments, controls, table, column, write_table, record, summary, read_xyz, atom_string
args = arguments(Path(__file__).parent)
c = controls(args.input)
from catalysis.thermo import chemical_potential
rows=[]
for t in column(args.input/'temperatures.csv','T_K'):
    for p in column(args.input/'pressures.csv','p_bar'):
        mu=float(chemical_potential(-t*c['gas_entropy_eV_K'],t,p))
        rows.append([t,p,mu,c['adsorption_energy_eV']-mu])
result={'columns':['T_K','p_bar','mu_minus_Egas_eV','adsorption_G_eV'],'scan':rows,
        'model':'constant gas entropy approximation; standard pressure 1 bar'}

from catalysis.teaching_io import export_tables
export_tables(args.output, result)
record(args, result, '\n'.join(summary(result)) + '\nTables and arrays are saved alongside this report.')
