"""Thermodynamically consistent A(g)+* ⇌ A* ⇌ B* ⇌ B(g)+* cycle.

Energies are free energies relative to A(g)+*. Gas activities p/p° are
explicit. Transition-state perturbations change both forward and reverse rates.
"""
import numpy as np
from scipy.integrate import solve_ivp
from .kinetics import tst
from .units import kbt, KB

DEFAULT = {'states_eV': [0., -.30, -.15], 'product_eV': -.10,
           'transition_states_eV': [.15, .45, .55]}


def constants(model, temperature):
    states = np.asarray(model['states_eV'], dtype=float)
    ts = np.asarray(model['transition_states_eV'], dtype=float)
    left = states
    right = np.array([states[1], states[2], model['product_eV']])
    if len(states) != 3 or len(ts) != 3 or np.any(ts < np.maximum(left, right)):
        raise ValueError('Three transition states must lie above their neighboring states')
    forward, reverse = tst(ts-left, temperature), tst(ts-right, temperature)
    return forward, reverse


def generator(model, temperature, pa=1., pb=.01):
    if pa <= 0 or pb <= 0:
        raise ValueError('Gas activities must be positive')
    f, r = constants(model, temperature)
    # Directed edge rates on [*, A*, B*]. Columns sum to zero.
    q = np.zeros((3,3))
    for i, j, rate in [(0,1,f[0]*pa), (1,0,r[0]), (1,2,f[1]),
                       (2,1,r[1]), (2,0,f[2]), (0,2,r[2]*pb)]:
        q[j,i] += rate; q[i,i] -= rate
    return q, f, r


def steady_state(model, temperature, pa=1., pb=.01):
    q, f, r = generator(model, temperature, pa, pb)
    matrix = q.copy(); matrix[-1] = 1
    rhs = np.array([0.,0.,1.])
    theta = np.linalg.solve(matrix, rhs)
    rates = np.array([f[0]*pa*theta[0]-r[0]*theta[1],
                      f[1]*theta[1]-r[1]*theta[2], f[2]*theta[2]-r[2]*pb*theta[0]])
    return {'coverages': theta.tolist(), 'TOF_s^-1': float(rates[-1]),
            'elementary_rates_s^-1': rates.tolist(), 'balance_residual_s^-1': float(np.linalg.norm(q@theta)),
            'forward_s^-1': f.tolist(), 'reverse_s^-1': r.tolist()}


def integrate(model, temperature, pa=1., pb=.01, initial=(1.,0.,0.)):
    q, _, _ = generator(model, temperature, pa, pb)
    rates = -np.linalg.eigvals(q).real
    slow = min(rates[rates > max(rates)*1e-12])
    times = np.r_[0., np.geomspace(1e-5/slow, 30/slow, 100)]
    sol = solve_ivp(lambda t,y:q@y, (0,times[-1]), initial, method='BDF',
                    jac=lambda t,y:q, t_eval=times, rtol=1e-9, atol=1e-12)
    if not sol.success:
        raise RuntimeError(sol.message)
    return {'time_s': sol.t.tolist(), 'coverages': sol.y.T.tolist()}


def response(model, temperature, pa=1., pb=.01, delta=.002):
    def lograte(t, a, b, m=model):
        rate = steady_state(m,t,a,b)['TOF_s^-1']
        if rate <= 0:
            raise ValueError('Log sensitivity requires positive net forward TOF')
        return np.log(rate)
    h = 1e-3
    orders = [(lograte(temperature,pa*np.exp(h),pb)-lograte(temperature,pa*np.exp(-h),pb))/(2*h),
              (lograte(temperature,pa,pb*np.exp(h))-lograte(temperature,pa,pb*np.exp(-h)))/(2*h)]
    invt = 1/temperature
    apparent = -KB*(lograte(1/(invt+h*invt),pa,pb)-lograte(1/(invt-h*invt),pa,pb))/(2*h*invt)
    control = []
    for i in range(3):
        logs = []
        for sign in [-1,1]:
            m = {**model, 'transition_states_eV': list(model['transition_states_eV'])}
            m['transition_states_eV'][i] += sign*delta
            logs.append(lograte(temperature,pa,pb,m))
        control.append(float(-kbt(temperature)*(logs[1]-logs[0])/(2*delta)))
    return {'reaction_orders_A_B': orders, 'apparent_activation_eV': float(apparent),
            'degree_of_rate_control': control}
