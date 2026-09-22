"""ASE reads structures; GPAW supplies electronic energies and forces."""
from pathlib import Path
from ase.io import read,write
from ase.optimize import BFGS
import numpy as np
from .surfaces import calculator
from .teaching_io import controls,table,write_table


def calculate_case(folder,output):
    folder,output=Path(folder),Path(output);output.mkdir(parents=True,exist_ok=True)
    import tomllib
    config=tomllib.loads((folder/'calculator.toml').read_text())
    if config.get('backend')!='gpaw':raise ValueError('This native DFT project requires backend=gpaw')
    energies={};structures={}
    for name in ['clean','H2',*config['sites']]:
        path=folder/(name+'.extxyz' if name=='H2' else name+'.POSCAR')
        atoms=read(path,format=None if name=='H2' else 'vasp')
        options={**config,'kpts':[1,1,1]} if name=='H2' else config
        atoms.calc=calculator(options,output/(name+'-gpaw.txt'))
        if not BFGS(atoms,logfile=str(output/(name+'-opt.txt'))).run(fmax=.02 if name=='H2' else config['fmax'],steps=250):
            raise RuntimeError(f'{name}: forces not converged')
        energies[name]=atoms.get_potential_energy();structures[name]=atoms
        write(output/(name+'-relaxed.extxyz'),atoms)
    return [{'site':site,'clean_eV':energies['clean'],'H2_eV':energies['H2'],'total_eV':energies[site],
             'force_max_eV_A':float(np.linalg.norm(structures[site].get_forces(),axis=1).max()),
             **dict(zip(['Hx_A','Hy_A','Hz_A'],structures[site].positions[-1]))} for site in config['sites']]


def adsorption_analysis(cases,rows,tolerance):
    results={}
    for case in cases:
        selected=[r for r in rows if r['scenario']==case['scenario']]
        sites=[]
        for row in selected:
            ec,eg,ea=[float(row[k]) for k in ['clean_eV','H2_eV','total_eV']]
            sites.append({'initial_site':row['site'],'total_eV':ea,'adsorption_eV':ea-ec-.5*eg,
                          'force_max_eV_A':float(row['force_max_eV_A']),
                          'final_H_position_A':[float(row[k]) for k in ['Hx_A','Hy_A','Hz_A']]})
        results[case['scenario']]={'backend':'gpaw','coverage_ML':float(case['coverage_ML']),
                                  'clean_eV':ec,'H2_eV':eg,'sites':sites}
    baseline=results['baseline'];sweep=[]
    for case in cases[1:]:
        energy=results[case['scenario']]['sites'][0]['adsorption_eV']
        sweep.append({'parameter':case['parameter'],'value':case['value'],'adsorption_eV':energy,
                      'delta_from_baseline_eV':energy-baseline['sites'][0]['adsorption_eV']})
    return {'backend':'gpaw','baseline':baseline,'sweep':sweep,'tolerance_eV':tolerance,
            'all_variations_within_tolerance':all(abs(r['delta_from_baseline_eV'])<tolerance for r in sweep)} if sweep else baseline
