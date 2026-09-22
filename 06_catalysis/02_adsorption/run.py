"""Analyze actual PBE energy records, or run GPAW on supplied POSCAR structures."""
from pathlib import Path
from catalysis.teaching_io import arguments,controls,table,write_table,record,summary,export_tables
from catalysis.native_dft import calculate_case,adsorption_analysis
args=arguments(Path(__file__).parent);c=controls(args.input)
if c.get('backend')!='gpaw':raise ValueError('The native PBE project requires backend=gpaw')
cases=table(args.input/'cases.csv')
if args.calculate:
    rows=[]
    for case in cases:
        rows.extend([{'scenario':case['scenario'],**r} for r in calculate_case(args.input/case['directory'],args.output/case['scenario'])])
    write_table(args.output/'energies.csv',list(rows[0]),[list(r.values()) for r in rows])
else:rows=table(args.input/'energies.csv')
result=adsorption_analysis(cases,rows,c['tolerance_eV'])
result['execution']='New GPAW calculations from native structures' if args.calculate else 'Analysis of previously executed PBE calculations; see input/DATA_SOURCE.md'
export_tables(args.output,result)
record(args,result,'\n'.join(summary(result))+'\nEach adsorption energy subtracts its own clean slab and half its own H2 reference.\nA slab thickness change also changes relaxation; a lateral cell change changes coverage.')
