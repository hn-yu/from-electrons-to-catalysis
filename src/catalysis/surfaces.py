"""Identical ASE workflows for explicitly labelled EMT emulation and GPAW DFT."""
from pathlib import Path
import numpy as np


def calculator(config, log):
    backend = config.get('backend','emt')
    if backend == 'emt':
        from ase.calculators.emt import EMT
        return EMT()
    if backend == 'gpaw':
        from gpaw import GPAW, PW, FermiDirac
        return GPAW(mode=PW(config.get('cutoff_eV',300)), xc='PBE',
                    kpts=tuple(config.get('kpts',[3,3,1])),
                    occupations=FermiDirac(config.get('smearing_eV',.1)),
                    convergence={'energy':1e-6}, txt=str(log))
    raise ValueError('backend must be emt or gpaw; no silent fallback')


def eos(config, workdir):
    from ase.build import bulk
    from ase.eos import EquationOfState
    from ase.units import GPa
    rows = []
    for a in config['lattice_constants_A']:
        atoms = bulk(config['element'],'fcc',a=a)
        atoms.calc = calculator(config, Path(workdir)/f'eos-{a}.txt')
        rows.append([a, atoms.get_volume(), atoms.get_potential_energy()])
    volume, energy, modulus = EquationOfState(np.array(rows)[:,1],np.array(rows)[:,2],eos='birchmurnaghan').fit()
    if not min(np.array(rows)[:,1]) < volume < max(np.array(rows)[:,1]):
        raise RuntimeError('EOS minimum is outside sampled volume range')
    return {'backend':config['backend'], 'scan_columns':['a_A','volume_A3_atom','energy_eV_atom'],
            'scan':rows, 'a0_A':float((4*volume)**(1/3)), 'bulk_modulus_GPa':float(modulus/GPa)}


def adsorption(config, workdir):
    from ase.build import fcc111, add_adsorbate, molecule
    from ase.constraints import FixAtoms
    from ase.optimize import BFGS
    from ase.io import write
    workdir = Path(workdir); workdir.mkdir(parents=True,exist_ok=True)
    size = tuple(config.get('size',[2,2,3])); layers = size[2]
    clean = fcc111('Cu',size=size,a=config.get('lattice_A',3.61),vacuum=config.get('vacuum_A',8.))
    fixed = config.get('fixed_layers',1)
    clean.set_constraint(FixAtoms(mask=clean.get_tags() > layers-fixed))
    clean.calc = calculator(config,workdir/'clean.txt')
    if not BFGS(clean,logfile=str(workdir/'clean-opt.txt')).run(fmax=config.get('fmax',.04),steps=200):
        raise RuntimeError('Clean slab relaxation failed')
    ec = clean.get_potential_energy()
    gas = molecule('H2'); gas.center(vacuum=4.)
    gas_config = {**config,'kpts':[1,1,1]}
    gas.calc = calculator(gas_config,workdir/'H2.txt')
    if not BFGS(gas,logfile=str(workdir/'H2-opt.txt')).run(fmax=.02,steps=100):
        raise RuntimeError('H2 reference relaxation failed')
    eg = gas.get_potential_energy()
    rows = []
    for site in config.get('sites',['ontop','bridge','fcc','hcp']):
        atoms = clean.copy(); add_adsorbate(atoms,'H',config.get('height_A',1.5),site)
        atoms.calc = calculator(config,workdir/f'{site}.txt')
        ok = BFGS(atoms,logfile=str(workdir/f'{site}-opt.txt')).run(fmax=config.get('fmax',.04),steps=250)
        if not ok:
            raise RuntimeError(f'{site} relaxation failed')
        energy = atoms.get_potential_energy()
        write(workdir/f'{site}.extxyz',atoms)
        rows.append({'initial_site':site, 'total_eV':float(energy), 'adsorption_eV':float(energy-ec-.5*eg),
                     'final_H_position_A':atoms.positions[-1].tolist(),
                     'force_max_eV_A':float(np.linalg.norm(atoms.get_forces(),axis=1).max())})
    return {'backend':config['backend'], 'reference':'E(slab+H)-E(slab)-0.5 E(H2)',
            'coverage_ML':1/(size[0]*size[1]), 'clean_eV':float(ec), 'H2_eV':float(eg), 'sites':rows,
            'scope':'EMT is a workflow emulator, not a DFT adsorption prediction.' if config['backend']=='emt' else 'PBE slab calculation; inspect convergence sweep before interpreting chemistry.'}


def convergence(config, workdir):
    baseline = config['baseline']; runs = []
    # Independently vary one setting, retaining reference energies in each evaluation.
    reference = adsorption(baseline,Path(workdir)/'baseline')
    base_energy = reference['sites'][0]['adsorption_eV']
    for parameter, values in config['sweeps'].items():
        for i,value in enumerate(values):
            setting = {**baseline,parameter:value}
            result = adsorption(setting,Path(workdir)/f'{parameter}-{i}')
            energy = result['sites'][0]['adsorption_eV']
            runs.append({'parameter':parameter,'value':value,'adsorption_eV':energy,
                         'delta_from_baseline_eV':energy-base_energy})
    tolerance = config['tolerance_eV']
    return {'backend':baseline['backend'], 'baseline':reference, 'sweep':runs, 'tolerance_eV':tolerance,
            'all_variations_within_tolerance':bool(all(abs(r['delta_from_baseline_eV'])<tolerance for r in runs)),
            'interpretation':'Agreement with one baseline does not establish an asymptotic convergence plateau; extend failing axes.'}
