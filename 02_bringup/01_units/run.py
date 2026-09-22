"""Read scientific input files, execute the stated method, and report observables."""
from pathlib import Path
import numpy as np
from catalysis.teaching_io import arguments, controls, table, column, write_table, record, summary, read_xyz, atom_string
args = arguments(Path(__file__).parent)
c = controls(args.input)
from catalysis.units import convert, kbt
from ase import units as au
rows=[]
for r in table(args.input/'conversions.csv'):
    value=float(r['value']); own=float(convert(value,r['from_unit'],r['to_unit']))
    factors={'eV':1.,'Hartree':au.Hartree,'kJ/mol':au.kJ/au.mol,'kcal/mol':au.kcal/au.mol,'cm^-1':au.invcm,'bar':1e5,'Pa':1.,'ps':1000.,'fs':1.}
    reference=value*factors[r['from_unit']]/factors[r['to_unit']]
    rows.append({**r,'own':own,'ASE':reference,'difference':own-reference})
result={'conversions':rows,'thermal_scales':[{'T_K':t,'kBT_eV':float(kbt(t))} for t in column(args.input/'temperatures.csv','T_K')]}

from catalysis.teaching_io import export_tables
export_tables(args.output, result)
record(args, result, '\n'.join(summary(result)) + '\nTables and arrays are saved alongside this report.')
