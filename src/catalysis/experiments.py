"""Executable experiments. Inputs are JSON; every runner records the full input and versions."""
from pathlib import Path
import numpy as np
from . import units, electronic, thermo, kinetics, network, sampling
from .potentials import Morse, Harmonic, MullerBrown, LennardJones


def units_experiment(c, work):
    return {'temperatures_K':c['temperatures_K'], 'kBT_eV':units.kbt(c['temperatures_K']).tolist(),
            'conversions':[{**r,'result':float(units.convert(r['value'],r['from'],r['to']))} for r in c['conversions']]}


def forces(c, work):
    potential = Morse(**c['potential'])
    rows = []
    for x in c['positions_A']:
        analytic = float(potential.force(x)); numeric = float(__import__('catalysis.potentials',fromlist=['finite_force']).finite_force(potential,x,c['step_A']))
        rows.append([x,potential.energy(x),analytic,numeric,abs(analytic-numeric)])
    return {'columns':['x_A','E_eV','analytic_force_eV_A','finite_force_eV_A','absolute_error'], 'scan':rows}


def finite_differences(c, work):
    from .potentials import finite_force
    p = Morse(); x = c['position_A']; exact = float(p.force(x))
    return {'analytic_force':exact, 'columns':['step_A','absolute_error'],
            'scan':[[float(h),abs(float(finite_force(p,x,h))-exact)] for h in np.logspace(*c['log10_step_range'])]}


def schrodinger(c, work):
    results = {}
    for kind in ['box','harmonic','finite_well','double_well']:
        x,e,psi = electronic.schrodinger(kind,**c)
        results[kind] = {'x_bohr':x.tolist(),'energies_Hartree':e.tolist(),'wavefunctions':psi.T.tolist(),
                         'nodes':[int(np.sum(v[1:]*v[:-1] < 0)) for v in psi.T]}
    return results


def lcao(c, work):
    e,v = electronic.lcao(c['H_Hartree'],c['S'])
    return {'energies_Hartree':e.tolist(),'coefficients':v.tolist(),
            'orthonormality':(v.T@np.array(c['S'])@v).tolist(),
            'basis_vector_Rayleigh_Hartree':(np.diag(c['H_Hartree'])/np.diag(c['S'])).tolist()}


def scf(c, work):
    return {r['name']:electronic.rhf(r['atom'],c['basis'],r.get('charge',0)) for r in c['molecules']}


def partition(c, work):
    return {'two_level':[{'T_K':t,**thermo.partition(c['energies_eV'],t,c['degeneracies'])} for t in c['temperatures_K']],
            'oscillator':[{'T_K':t,**thermo.oscillator(c['quantum_eV'],t)} for t in c['temperatures_K']]}


def chemical_potential(c, work):
    rows = []
    for t in c['temperatures_K']:
        # μ° toy thermochemistry: Egas - T Sgas; constant S approximation is declared.
        mu0 = -t*c['gas_entropy_eV_K']
        for p in c['pressures_bar']:
            mu = float(thermo.chemical_potential(mu0,t,p))
            dg = c['adsorption_energy_eV']-mu
            rows.append([t,p,mu,dg])
    return {'columns':['T_K','p_bar','mu_relative_to_Egas_eV','adsorption_deltaG_eV'], 'scan':rows,
            'model':'constant standard gas entropy; immobile adsorbate; no lateral interactions'}


def surface_phase(c, work):
    return thermo.surface_phase(c['states'],np.linspace(*c['mu_grid_eV']))


def optimizer(c, work):
    return {'morse':[kinetics.minimize(Morse(),[x]) for x in c['morse_starts_A']],
            'muller_brown':[kinetics.minimize(MullerBrown(),x) for x in c['mb_starts']]}


def dynamics(c, work):
    rows = []
    for dt in c['timesteps']:
        trajectory = kinetics.verlet(Harmonic(),[1.],[0.],dt,c['steps'])
        rows.append({'dt':dt,'max_energy_error':float(np.max(abs(trajectory[:,1]-.5))),
                     'final_energy':float(trajectory[-1,1])})
    cluster = kinetics.verlet(LennardJones(),[[0.,0.,0.],[1.2,0.,0.]],[[0.,.03,0.],[0.,-.03,0.]],.002,2000)
    np.savetxt(Path(work)/'cluster.csv',cluster,delimiter=',',header='time,energy,x1,y1,z1,x2,y2,z2',comments='')
    return {'units':'reduced units (m=k=1 for harmonic; LJ sigma=epsilon=m=1)',
            'timestep_sweep':rows,'cluster_energy_span':float(np.ptp(cluster[:,1]))}


def hessian(c, work):
    from scipy.optimize import root
    p = MullerBrown()
    minimum = np.array(kinetics.minimize(p,c['minimum_start'])['x'])
    saddle_solution = root(lambda x:-p.force(x),c['saddle_start'])
    if not saddle_solution.success or np.linalg.norm(p.force(saddle_solution.x)) > 1e-6:
        raise RuntimeError('Saddle search failed')
    results = {}
    for name,point in [('minimum',minimum),('saddle',saddle_solution.x)]:
        h,e,v = kinetics.hessian(p,point)
        results[name] = {'point':point.tolist(),'hessian':h.tolist(),'mass_weighted_eigenvalues':e.tolist(),
                         'modes':v.tolist(),'negative_modes':int(np.sum(e < -1e-6))}
    h,e,_ = kinetics.hessian(Morse(),[.74],mass=c['morse_mass_amu'])
    angular = np.sqrt(e*units.EV_J/(units.AMU_KG*1e-20))
    results['morse_frequency_cm^-1'] = (angular/(2*np.pi*2.99792458e10)).tolist()
    return results


def neb(c, work):
    from ase import Atoms
    from ase.calculators.calculator import Calculator, all_changes
    from ase.mep import NEB
    from ase.optimize import FIRE
    p = MullerBrown()
    endpoints = [kinetics.minimize(p,v)['x'] for v in c['endpoints']]
    own = kinetics.neb(p,*endpoints,images=c['images'])
    class Surface(Calculator):
        implemented_properties = ['energy','forces']
        def calculate(self,atoms=None,properties=('energy',),system_changes=all_changes):
            super().calculate(atoms,properties,system_changes)
            point = self.atoms.positions[0,:2]
            self.results = {'energy':p.energy(point),'forces':np.array([[*p.force(point),0.]])}
    images = []
    for point in np.linspace(*endpoints,c['images']):
        atom = Atoms('H',positions=[[*point,0.]]); atom.calc = Surface(); images.append(atom)
    band = NEB(images,k=5.,method='improvedtangent')
    if not FIRE(band,dt=.005,maxstep=.03,logfile=str(Path(work)/'ase-neb.txt')).run(fmax=2e-4,steps=40000):
        raise RuntimeError('ASE NEB did not converge')
    energies = [a.get_potential_energy() for a in images]
    return {'own':own,'ASE_barrier_eV':max(energies)-energies[0],
            'barrier_difference_eV':own['barrier_eV']-(max(energies)-energies[0]),
            'scope':'2D benchmark; production atom diffusion requires validated endpoints and a separate potential.'}


def tst(c, work):
    rows = []
    for t in c['temperatures_K']:
        for barrier in np.linspace(*c['barriers_eV']):
            rate = float(kinetics.tst(barrier,t))
            rows.append([t,float(barrier),rate,1/rate,float(kinetics.arrhenius(barrier,t,c['prefactor_s^-1']))])
    np.savetxt(Path(work)/'barrier-timescale.csv',rows,delimiter=',',header='T_K,barrier_eV,TST_s^-1,timescale_s,Arrhenius_s^-1',comments='')
    return {'columns':['T_K','barrier_eV','TST_s^-1','timescale_s','Arrhenius_s^-1'],'scan':rows}


def umbrella(c, work):
    return {'one_dimension':sampling.umbrella(**c),
            'hidden_coordinate':sampling.umbrella(**{**c,'dimensions':2}),
            'bad_coordinate':sampling.bad_coordinate(c['temperature'],c['seed'])}


def mep_fes(c, work):
    x = np.linspace(-1.4,1.4,201); mep = .15*(x*x-1)**2
    rows = []
    for t in c['temperatures_K']:
        f = mep+.5*units.kbt(t)*np.log(1+x*x); f -= f.min()
        # F minimum moves with T; use the actual sampled minimum, not the 0 K endpoint.
        rows.append({'T_K':t,'F_eV':f.tolist(),'barrier_eV':float(f[len(x)//2]-f.min())})
    return {'x':x.tolist(),'MEP_eV':mep.tolist(),'MEP_barrier_eV':.15,'finite_temperature':rows}


def reaction_network(c, work):
    f,r = network.constants(c['model'],c['temperature_K'])
    dg = np.diff([*c['model']['states_eV'],c['model']['product_eV']])
    return {'species':['vacancy','A_ads','B_ads'], 'stoichiometry':[[-1,0,1],[1,-1,0],[0,1,-1]],
            'deltaG_eV':dg.tolist(),'forward_s^-1':f.tolist(),'reverse_s^-1':r.tolist(),
            'detailed_balance_log_residual':(np.log(f/r)+dg/units.kbt(c['temperature_K'])).tolist()}


def microkinetics(c, work):
    t = c['temperature_K']; m = c['model']; pa = c['pA_bar']; pb = c['pB_bar']
    return {'steady_state':network.steady_state(m,t,pa,pb),'integration':network.integrate(m,t,pa,pb),
            'response':network.response(m,t,pa,pb),
            'sweep':[{'T_K':temp,'pA_bar':pressure,**network.steady_state(m,temp,pressure,pb)}
                     for temp in c['temperatures_K'] for pressure in c['pressures_bar']],
            'selectivity':'Only one product in this model; selectivity is identically 1.'}


def rate_control(c, work):
    m = c['model']; t = c['temperature_K']
    reference = network.steady_state(m,t)['TOF_s^-1']; rows = []
    for name in ['states_eV','transition_states_eV']:
        for index in (range(1,3) if name=='states_eV' else range(3)):
            for shift in [-.1,.1]:
                changed = {**m,name:list(m[name])}; changed[name][index] += shift
                rate = network.steady_state(changed,t)['TOF_s^-1']
                rows.append({'parameter':name,'index':index,'shift_eV':shift,'TOF_ratio':rate/reference})
    barriers = np.array(m['transition_states_eV'])-np.array(m['states_eV'])
    return {'forward_barriers_eV':barriers.tolist(),'response':network.response(m,t), 'perturbations':rows}


def periodic(c, work):
    from .surfaces import eos
    result = eos(c,work)
    if 'sweeps' in c:
        result['convergence_sweep'] = []
        for name,values in c['sweeps'].items():
            for i,value in enumerate(values):
                folder = Path(work)/f'{name}-{i}'; folder.mkdir(exist_ok=True)
                value_result = eos({**c,name:value},folder)
                result['convergence_sweep'].append({'parameter':name,'value':value,**value_result})
    return result


def adsorption(c, work):
    from .surfaces import adsorption as run
    return run(c,work)


def slab(c, work):
    from .surfaces import convergence
    return convergence(c,work)


def hf_failures(c, work):
    from .quantum import hf_failures as run
    return run(c)


def dft(c, work):
    from .quantum import dft_comparison
    return dft_comparison(c)


def molecular_thermo(c, work):
    from .quantum import molecular_thermo as run
    return run(c)


EXPERIMENTS = {f.__name__:f for f in [units_experiment,forces,finite_differences,schrodinger,lcao,scf,
    partition,chemical_potential,surface_phase,optimizer,dynamics,hessian,neb,tst,umbrella,mep_fes,
    reaction_network,microkinetics,rate_control,periodic,adsorption,slab,hf_failures,dft,molecular_thermo]}
