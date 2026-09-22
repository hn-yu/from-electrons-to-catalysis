"""Independent native Cantera mechanism and coverage solver for the teaching cycle."""
from pathlib import Path
import numpy as np
from .teaching_io import table
from .units import KB, H


def model_from_tables(folder):
    states = {r['state']:float(r['G0_eV']) for r in table(Path(folder)/'states.csv')}
    return {'states_eV':[states[n] for n in ['vacancy','A_ads','B_ads']],
            'product_eV':states['B_gas'],
            'transition_states_eV':[float(r['TS_eV']) for r in table(Path(folder)/'transitions.csv')]}


def write_mechanism(folder):
    """Export an explicit reviewable YAML; the reference solver reads this file only."""
    import cantera as ct
    from ruamel.yaml import YAML
    m = model_from_tables(folder)
    scale = ct.avogadro*ct.electron_charge  # eV/particle -> J/kmol
    species=[]
    for name,energy in zip(['A_g','B_g','X','A_ads','B_ads'],[0,m['product_eV'],*m['states_eV']]):
        species.append({'name':name,'composition':{} if name=='X' else {'H':1},
                        'thermo':{'model':'constant-cp','T0':'298.15 K','h0':f'{energy*scale:.16g} J/kmol',
                                  's0':'0 J/kmol/K','cp0':f'{0 if name=="X" else 2.5*ct.gas_constant:.16g} J/kmol/K',
                                  'reference-pressure':'1 bar'}})
    alpha=KB/H
    data={'description':'Abstract isomer cycle, not hydrogen chemistry. Equal occupied-species cp cancels in reaction free energies.',
          'units':{'length':'m','quantity':'kmol','activation-energy':'J/kmol'},
          'phases':[{'name':'gas','thermo':'ideal-gas','elements':['H'],'species':['A_g','B_g'],
                     'state':{'T':600.,'P':'1.01 bar','X':{'A_g':1.,'B_g':.01}}},
                    {'name':'surface','thermo':'ideal-surface','adjacent-phases':['gas'],'elements':['H'],
                     'species':['X','A_ads','B_ads'],'kinetics':'surface','reactions':'all',
                     'site-density':'2.7e-8 kmol/m^2','state':{'T':600.,'coverages':{'X':1}}}],
          'species':species,'reactions':[]}
    for i,equation in enumerate(['A_g + X <=> A_ads','A_ads <=> B_ads','B_ads <=> B_g + X']):
        data['reactions'].append({'equation':equation,'rate-constant':{
            'A':alpha*ct.gas_constant/1e5 if i==0 else alpha,'b':2 if i==0 else 1,
            'Ea':(m['transition_states_eV'][i]-m['states_eV'][i])*scale}})
    with (Path(folder)/'mechanism.yaml').open('w') as stream:YAML().dump(data,stream)


def solve(path, temperature, pa=1., pb=.01, multipliers=None):
    import cantera as ct
    surface=ct.Interface(str(path),'surface');gas=surface.adjacent['gas']
    gas.TPX=temperature,(pa+pb)*1e5,{'A_g':pa,'B_g':pb}
    surface.TP=temperature,gas.P
    surface.coverages=[1,0,0]
    for i,m in enumerate(multipliers or [1.,1.,1.]):surface.set_multiplier(m,i)
    surface.advance_coverages_to_steady_state()
    rates=surface.net_rates_of_progress/surface.site_density
    return {'coverages':surface.coverages.tolist(),'TOF_s^-1':float(rates[-1]),
            'elementary_rates_s^-1':rates.tolist()}


def rate_control(path, temperature, delta=1e-3):
    values=[]
    for i in range(3):
        rates=[]
        for sign in [-1,1]:
            multipliers=[1.,1.,1.];multipliers[i]=np.exp(sign*delta)
            rates.append(solve(path,temperature,multipliers=multipliers)['TOF_s^-1'])
        values.append(float((np.log(rates[1])-np.log(rates[0]))/(2*delta)))
    return values
