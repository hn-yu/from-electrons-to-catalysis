"""Optimization, dynamics, curvature, nudged bands and elementary rates."""
import numpy as np
from .units import H, kbt


def minimize(potential, initial, tolerance=1e-6, maxiter=20000):
    x = np.array(initial, dtype=float)
    history = []
    for iteration in range(maxiter):
        e, f = potential.energy(x), potential.force(x)
        history.append([iteration, e, float(np.linalg.norm(f))])
        if np.linalg.norm(f) < tolerance:
            return {'x': x.tolist(), 'energy': e, 'iterations': iteration, 'force_norm': history[-1][2]}
        step = .1
        for _ in range(60):
            trial = x+step*f
            if potential.energy(trial) <= e-1e-4*step*np.sum(f*f):
                x = trial
                break
            step *= .5
        else:
            raise RuntimeError('Line search failed')
    raise RuntimeError('Optimizer did not converge')


def verlet(potential, x, velocity, dt=.01, steps=1000, mass=1.):
    if dt <= 0 or steps < 1 or np.any(np.asarray(mass) <= 0):
        raise ValueError('Positive dt, mass and steps required')
    x, v = np.array(x, dtype=float), np.array(velocity, dtype=float)
    m = np.asarray(mass)
    f = potential.force(x)
    rows = []
    for i in range(steps+1):
        energy = potential.energy(x)+float(.5*np.sum(m*v*v))
        rows.append([i*dt, energy, *x.ravel()])
        if i == steps:
            break
        x += dt*v+.5*dt*dt*f/m
        new = potential.force(x)
        v += .5*dt*(f+new)/m
        f = new
    return np.array(rows)


def hessian(potential, point, mass=1., step=1e-4):
    if step <= 0 or np.any(np.asarray(mass) <= 0):
        raise ValueError('Positive step and masses required')
    x = np.asarray(point, dtype=float)
    n = x.size
    h = np.zeros((n,n))
    for i in range(n):
        d = np.zeros(n); d[i] = step; d = d.reshape(x.shape)
        h[:,i] = -(potential.force(x+d)-potential.force(x-d)).ravel()/(2*step)
    m = np.broadcast_to(mass, x.shape).ravel()
    weighted = .5*(h+h.T)/np.sqrt(m[:,None]*m[None,:])
    eig, modes = np.linalg.eigh(weighted)
    return h, eig, modes


def neb(potential, start, end, images=19, spring=5., tolerance=2e-4, maxiter=40000):
    """Improved energy-weighted tangent, perpendicular true force, parallel springs; FIRE."""
    if images < 3 or spring <= 0:
        raise ValueError('Need >=3 images and positive spring')
    path = np.linspace(start, end, images)
    velocities = np.zeros_like(path)
    dt, dtmax, alpha, positive = .005, .04, .1, 0
    for iteration in range(maxiter):
        energies = np.array([potential.energy(p) for p in path])
        forces = np.zeros_like(path)
        for i in range(1, images-1):
            forward, backward = path[i+1]-path[i], path[i]-path[i-1]
            if energies[i+1] > energies[i] > energies[i-1]:
                tangent = forward
            elif energies[i+1] < energies[i] < energies[i-1]:
                tangent = backward
            else:
                de1, de2 = abs(energies[i+1]-energies[i]), abs(energies[i-1]-energies[i])
                hi, lo = max(de1,de2), min(de1,de2)
                tangent = forward*hi+backward*lo if energies[i+1] > energies[i-1] else forward*lo+backward*hi
            # Do not normalize forward/backward in-place: their lengths enter springs.
            tangent = tangent.copy()
            norm = np.linalg.norm(tangent)
            if norm < 1e-14:
                tangent = forward + backward
                norm = np.linalg.norm(tangent)
                if norm < 1e-14:
                    raise RuntimeError('Collapsed NEB images')
            tangent /= norm
            true = potential.force(path[i])
            forces[i] = true-(true@tangent)*tangent+spring*(np.linalg.norm(forward)-np.linalg.norm(backward))*tangent
        fmax = np.linalg.norm(forces, axis=1).max()
        if fmax < tolerance:
            return {'path': path.tolist(), 'energies_eV': energies.tolist(),
                    'barrier_eV': float(energies.max()-energies[0]), 'force_max': float(fmax), 'iterations': iteration}
        velocities += dt*forces
        power = np.sum(velocities*forces)
        if power > 0:
            positive += 1
            vnorm, fnorm = np.linalg.norm(velocities), np.linalg.norm(forces)
            velocities = (1-alpha)*velocities+alpha*vnorm/fnorm*forces
            if positive > 5:
                dt = min(dt*1.1, dtmax); alpha *= .99
        else:
            positive = 0; dt *= .5; alpha = .1; velocities[:] = 0
        displacement = dt*velocities
        largest = np.max(np.linalg.norm(displacement, axis=1))
        if largest > .03:
            displacement *= .03/largest
        path[1:-1] += displacement[1:-1]
    raise RuntimeError(f'NEB did not converge: fmax={fmax}')


def tst(barrier, temperature, transmission=1.):
    if not 0 < transmission <= 1:
        raise ValueError('Transmission coefficient must lie in (0,1]')
    kt = kbt(temperature)
    return transmission*kt/H*np.exp(-np.asarray(barrier)/kt)


def arrhenius(barrier, temperature, prefactor=1e13):
    if prefactor <= 0:
        raise ValueError('Prefactor must be positive')
    return prefactor*np.exp(-np.asarray(barrier)/kbt(temperature))
