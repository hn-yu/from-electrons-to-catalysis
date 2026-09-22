"""Numerical, physical and limiting-case checks, independent of stored example output."""
import numpy as np
import pytest
from scipy.linalg import expm
from catalysis import units, electronic, thermo, kinetics, network, sampling
from catalysis.potentials import Morse, Harmonic, MullerBrown, DoubleWell, LennardJones, finite_force

@pytest.mark.parametrize('source,target',[('eV','Hartree'),('cm^-1','kJ/mol'),('bar','Pa'),('ps','fs')])
def test_units_roundtrip(source,target):
    assert units.convert(units.convert(3.2,source,target),target,source) == pytest.approx(3.2)

def test_units_scales_and_domain():
    assert units.kbt(300) == pytest.approx(.025852,rel=1e-5)
    assert units.kbt(600) == 2*units.kbt(300)
    assert units.convert(1,'bar','Pa') == 1e5
    with pytest.raises(ValueError): units.convert(1,'bar','eV')
    with pytest.raises(ValueError): units.kbt(0)

@pytest.mark.parametrize('potential,point',[(Morse(),[.5]),(Morse(),[1.3]),(MullerBrown(),[-.3,.8]),
    (DoubleWell(),[.4,.3]),(LennardJones(),[[0.,0.,0.],[1.3,.1,0.]])])
def test_analytic_force(potential,point):
    np.testing.assert_allclose(potential.force(point),finite_force(potential,point),atol=2e-6,rtol=1e-6)

def test_morse_physics_and_limit():
    p=Morse()
    assert p.force(.5)>0 and p.force(1.)<0
    assert p.energy(.74)==-4.5
    assert p.energy(30.)==pytest.approx(0,abs=1e-12)
    assert p.force(.74)==0

def test_finite_difference_cancellation():
    p=Morse(); point=1.1
    errors=[abs(float(finite_force(p,point,h)-p.force(point))) for h in [1e-15,1e-5,.1]]
    assert errors[1]<min(errors[0],errors[2])*1e-3

@pytest.mark.parametrize('kind',['box','harmonic','finite_well','double_well'])
def test_schrodinger_normalization_nodes(kind):
    x,e,psi=electronic.schrodinger(kind,n=300)
    dx=x[1]-x[0]
    np.testing.assert_allclose(psi.T@psi*dx,np.eye(4),atol=1e-12)
    assert np.all(np.diff(e)>0)
    assert [np.sum(p[1:]*p[:-1]<0) for p in psi.T]==[0,1,2,3]

def test_schrodinger_analytic_and_grid_limit():
    _,coarse,_=electronic.schrodinger('box',n=100)
    _,fine,_=electronic.schrodinger('box',n=200)
    exact=np.arange(1,5)**2*np.pi**2/(2*12**2)
    assert np.max(abs(fine-exact))<np.max(abs(coarse-exact))/3.9
    _,e,_=electronic.schrodinger('harmonic',n=600)
    np.testing.assert_allclose(e,np.arange(4)+.5,atol=4e-4)
    _,e,_=electronic.schrodinger('double_well')
    assert 0<e[1]-e[0]<e[2]-e[1]

def test_lcao_residual_variational_and_no_overlap():
    h=np.array([[-1.,-.3],[-.3,-1.]])
    s=np.array([[1.,.2],[.2,1.]])
    e,c=electronic.lcao(h,s)
    np.testing.assert_allclose(h@c,s@c@np.diag(e),atol=1e-14)
    np.testing.assert_allclose(c.T@s@c,np.eye(2),atol=1e-14)
    assert e[0]<-1
    np.testing.assert_allclose(e,[-1.3/1.2,-.7/.8])
    np.testing.assert_allclose(electronic.lcao(h,np.eye(2))[0],[-1.3,-.7])
    with pytest.raises(ValueError):electronic.lcao(h,[[1.,1.],[1.,1.]])

def test_partition_identity_and_limits():
    r=thermo.partition([0,.1],300,[1,3])
    assert sum(r['populations'])==pytest.approx(1)
    assert r['U_eV']-r['F_eV']==pytest.approx(300*r['S_eV_K'])
    assert thermo.partition([0,.1],1,[1,3])['populations'][0]==pytest.approx(1)
    assert thermo.partition([0,.1],1e9,[1,3])['populations'][1]==pytest.approx(.75,abs=1e-6)
    shift=thermo.partition([10,10.1],300,[1,3])
    np.testing.assert_allclose(r['populations'],shift['populations'])
    assert shift['F_eV']-r['F_eV']==pytest.approx(10)

def test_oscillator_ladder_and_limits():
    t=300; q=.12
    exact=thermo.partition((np.arange(100)+.5)*q,t)
    r=thermo.oscillator(q,t)
    assert r['U_eV']==pytest.approx(exact['U_eV'])
    assert r['F_eV']==pytest.approx(exact['F_eV'])
    assert thermo.oscillator(q,1)['U_eV']==pytest.approx(.06)
    assert thermo.oscillator(q,1e7)['U_eV']/units.kbt(1e7)==pytest.approx(1,rel=1e-8)
    with pytest.raises(ValueError):thermo.oscillator([0],300)

def test_mu_slope_standard_state_and_domain():
    assert thermo.chemical_potential(-1,300,1)==-1
    assert thermo.chemical_potential(0,300,np.e)==pytest.approx(units.kbt(300))
    assert thermo.chemical_potential(0,300,1e-10)<0
    with pytest.raises(ValueError):thermo.chemical_potential(0,300,0)

def test_phase_envelope_limits():
    states=[{'name':'clean','energy_eV':0.,'adsorbates':0},{'name':'one','energy_eV':-.5,'adsorbates':1}]
    r=thermo.surface_phase(states,[-100,-.5,100])
    assert r['stable_state'][0]=='clean' and r['stable_state'][-1]=='one'
    assert r['grand_potential_eV'][0][1]==r['grand_potential_eV'][1][1]

def test_optimizer_minima_and_stationary_limit():
    for x in [.5,1.2]:
        result=kinetics.minimize(Morse(),[x])
        assert result['x'][0]==pytest.approx(.74,abs=1e-6)
    assert kinetics.minimize(Morse(),[.74])['iterations']==0
    a=kinetics.minimize(MullerBrown(),[-.6,1.4]); b=kinetics.minimize(MullerBrown(),[.6,0.])
    assert np.linalg.norm(np.array(a['x'])-b['x'])>1
    assert a['force_norm']<1e-6

def test_verlet_energy_scaling_physical_and_stability():
    spans=[]
    for dt in [.02,.01]:
        trajectory=kinetics.verlet(Harmonic(),[1.],[0.],dt,1000)
        spans.append(np.ptp(trajectory[:,1]))
    assert spans[0]/spans[1]==pytest.approx(4,rel=.01)
    unstable=kinetics.verlet(Harmonic(),[1.],[0.],2.1,100)
    assert unstable[-1,1]>1e10
    stationary=kinetics.verlet(Harmonic(),[0.],[0.],.1,10)
    assert np.max(abs(stationary[:,1:]))==0
    f=LennardJones().force([[0.,0.,0.],[1.2,.1,0.]])
    np.testing.assert_allclose(f.sum(axis=0),0,atol=1e-15)

def test_hessian_curvature_symmetry_and_mass():
    p=Morse(); h,e,_=kinetics.hessian(p,[.74])
    assert h[0,0]==pytest.approx(2*4.5*1.8**2,rel=1e-6)
    _,heavy,_=kinetics.hessian(p,[.74],mass=4)
    assert heavy[0]==pytest.approx(e[0]/4)
    h,e,_=kinetics.hessian(DoubleWell(),[0.,0.])
    np.testing.assert_allclose(h,h.T,atol=1e-10)
    assert sum(e<0)==1

def test_neb_straight_analytic_limit():
    p=DoubleWell()
    result=kinetics.neb(p,[-1.,0.],[1.,0.],images=11)
    assert result['barrier_eV']==pytest.approx(.15)
    assert result['force_max']<1e-8
    assert result['path'][0]==[-1.,0.] and result['path'][-1]==[1.,0.]

def test_tst_prefactor_ratio_temperature_and_arrhenius():
    assert kinetics.tst(0,600)==pytest.approx(units.kbt(600)/units.H)
    assert kinetics.tst(.6,600)/kinetics.tst(.5,600)==pytest.approx(np.exp(-.1/units.kbt(600)))
    assert kinetics.tst(1,1000)>kinetics.tst(1,300)
    assert kinetics.arrhenius(0,300)==1e13

@pytest.mark.parametrize('t',[300,600,1000])
def test_network_detailed_balance_site_conservation_equilibrium(t):
    m=network.DEFAULT
    f,r=network.constants(m,t)
    dg=np.diff([*m['states_eV'],m['product_eV']])
    np.testing.assert_allclose(np.log(f/r),-dg/units.kbt(t),atol=1e-13)
    pb=np.exp(-m['product_eV']/units.kbt(t))
    result=network.steady_state(m,t,1.,pb)
    assert abs(result['TOF_s^-1'])<1e-9*max(f)
    q,_,_=network.generator(m,t)
    # Rates reach 1e12/s; absolute cancellation error is not a physical imbalance.
    np.testing.assert_allclose(q.sum(axis=0)/np.max(abs(q)),0,atol=1e-15)

def test_microkinetic_independent_matrix_exponential_and_ode():
    m=network.DEFAULT;t=600
    result=network.steady_state(m,t)
    theta=np.array(result['coverages'])
    assert np.all(theta>0) and theta.sum()==pytest.approx(1)
    np.testing.assert_allclose(result['elementary_rates_s^-1'],result['TOF_s^-1'],rtol=1e-8)
    sol=network.integrate(m,t)
    np.testing.assert_allclose(sol['coverages'][-1],theta,atol=1e-8)
    q,_,_=network.generator(m,t)
    np.testing.assert_allclose(expm(q*sol['time_s'][-1])@np.array([1.,0.,0.]),theta,atol=2e-8)

def test_rate_control_sum_and_small_perturbation_limit():
    result=network.response(network.DEFAULT,600,delta=.001)
    assert sum(result['degree_of_rate_control'])==pytest.approx(1,abs=1e-5)
    refined=network.response(network.DEFAULT,600,delta=.0005)
    np.testing.assert_allclose(result['degree_of_rate_control'],refined['degree_of_rate_control'],atol=1e-5)
    assert np.isfinite(result['apparent_activation_eV'])

def test_wham_exact_histograms_and_unbiased_limit():
    x=np.linspace(-1.5,1.5,61);kt=units.kbt(600)
    v=.15*(x*x-1)**2;centers=np.linspace(-1,1,7)
    bias=(x[None,:]-centers[:,None])**2
    weights=np.exp(-(v[None,:]+bias)/kt)
    counts=10000*weights/weights.sum(axis=1)[:,None]
    probability,iterations=sampling.wham(counts,bias,600)
    exact=np.exp(-v/kt);exact/=exact.sum()
    np.testing.assert_allclose(probability,exact,atol=1e-8)
    assert probability.sum()==pytest.approx(1) and iterations>1
    p,_=sampling.wham([[1,2,3]],[[0,0,0]],300)
    np.testing.assert_allclose(p,np.array([1,2,3])/6)
