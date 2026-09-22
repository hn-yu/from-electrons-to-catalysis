"""Seeded Metropolis umbrella sampling and log-domain histogram WHAM."""
import numpy as np
from scipy.special import logsumexp
from .units import kbt
from .potentials import DoubleWell


def wham(counts, bias, temperature, tolerance=1e-9, maxiter=20000):
    counts = np.asarray(counts, dtype=float)
    bias = np.asarray(bias, dtype=float)
    if counts.shape != bias.shape or np.any(counts < 0) or np.any(counts.sum(axis=1) <= 0):
        raise ValueError('Need nonnegative window/bin counts and matching biases')
    total = counts.sum(axis=0)
    active = total > 0
    kt = float(kbt(temperature))
    logn = np.log(counts.sum(axis=1))
    offsets = np.zeros(len(counts))
    for iteration in range(maxiter):
        logp = np.log(total[active])-logsumexp(logn[:,None]+(offsets[:,None]-bias[:,active])/kt, axis=0)
        logp -= logsumexp(logp)
        new = -kt*logsumexp(logp[None,:]-bias[:,active]/kt, axis=1)
        new -= new[0]
        if np.max(abs(new-offsets)) < tolerance:
            probability = np.zeros_like(total); probability[active] = np.exp(logp)
            return probability, iteration+1
        offsets = new
    raise RuntimeError('WHAM did not converge')


def umbrella(temperature=600., windows=13, steps=16000, burn=2000, seed=2026,
             dimensions=1, stiffness=2.):
    if steps <= burn or windows < 2 or dimensions not in (1,2):
        raise ValueError('Need production steps, multiple windows, and 1D or 2D')
    kt = float(kbt(temperature)); rng = np.random.default_rng(seed)
    potential = DoubleWell()
    centers = np.linspace(-1.5,1.5,windows)
    edges = np.linspace(-1.8,1.8,121); bins = (edges[1:]+edges[:-1])/2
    counts, accepted, hidden_means = [], [], []
    for center in centers:
        point = np.zeros(dimensions); point[0] = center
        def energy(x):
            return potential.energy(x)+.5*stiffness*(x[0]-center)**2
        old = energy(point); samples = []; hidden = []; accept = 0
        for i in range(steps):
            proposal = point+rng.normal(0,.16,dimensions)
            new = energy(proposal)
            if np.log(rng.random()) < -(new-old)/kt:
                point, old = proposal, new; accept += 1
            if i >= burn:
                samples.append(point[0])
                if dimensions == 2:
                    hidden.append(point[1])
        counts.append(np.histogram(samples, edges)[0]); accepted.append(accept/steps)
        hidden_means.append(float(np.mean(hidden)) if hidden else 0.)
    counts = np.array(counts)
    bias = .5*stiffness*(bins[None,:]-centers[:,None])**2
    p, iterations = wham(counts, bias, temperature)
    fes = np.full_like(p, np.nan); mask = p > 0
    fes[mask] = -kt*np.log(p[mask]); fes[mask] -= np.min(fes[mask])
    exact = .15*(bins*bins-1)**2
    if dimensions == 2:
        exact += .5*kt*np.log(1+bins*bins)
    exact -= exact.min()
    # Restrict comparison to well-sampled interior; histogram bins are correlated.
    selected = (abs(bins)<1.3)&(counts.sum(axis=0)>30)
    residual = fes[selected]-exact[selected]; residual -= residual.mean()
    return {'x': bins.tolist(), 'F_eV': [float(v) if np.isfinite(v) else None for v in fes],
            'exact_F_eV': exact.tolist(), 'counts': counts.tolist(), 'acceptance': accepted,
            'hidden_means': hidden_means, 'iterations': iterations,
            'shape_RMSE_eV': float(np.sqrt(np.mean(residual**2))),
            'adjacent_overlap_bins': [int(np.sum((counts[i]>0)&(counts[i+1]>0))) for i in range(windows-1)]}


def bad_coordinate(temperature=600., seed=2026, steps=10000):
    """x hides a double-well y with a >15 kBT barrier; two starts reveal nonmixing."""
    rng = np.random.default_rng(seed); kt = float(kbt(temperature)); results = []
    for initial in [-1.,1.]:
        x = np.array([0.,initial]); switches = 0; ys = []
        def energy(p):
            return .5*(p[0]-.4*p[1])**2+.8*(p[1]**2-1)**2
        e = energy(x)
        for _ in range(steps):
            trial = x+rng.normal(0,.08,2); en = energy(trial)
            if np.log(rng.random()) < -(en-e)/kt:
                switches += int(trial[1]*x[1] < 0); x, e = trial, en
            ys.append(x[1])
        results.append({'initial_y':initial, 'mean_y':float(np.mean(ys)), 'sign_switches':switches})
    return results
