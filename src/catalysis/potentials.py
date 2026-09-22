"""One energy/force contract shared by optimization, vibrations, MD and NEB."""
from dataclasses import dataclass
import numpy as np

@dataclass
class Morse:
    depth: float = 4.5
    alpha: float = 1.8
    equilibrium: float = 0.74

    def energy(self, x):
        z = np.exp(-self.alpha * (np.asarray(x) - self.equilibrium))
        return float(np.sum(self.depth * ((1 - z)**2 - 1)))

    def force(self, x):
        z = np.exp(-self.alpha * (np.asarray(x) - self.equilibrium))
        return -2 * self.depth * self.alpha * z * (1 - z)

@dataclass
class Harmonic:
    stiffness: float = 1.

    def energy(self, x):
        return float(0.5 * self.stiffness * np.sum(np.asarray(x)**2))

    def force(self, x):
        return -self.stiffness * np.asarray(x)

class MullerBrown:
    """Standard Müller–Brown surface, scaled by 0.01 to teaching eV units."""
    a = np.array([-1., -1., -6.5, .7])
    b = np.array([0., 0., 11., .6])
    c = np.array([-10., -10., -6.5, .7])
    centers = np.array([[1., 0.], [0., .5], [-.5, 1.5], [-1., 1.]])
    amplitudes = np.array([-2., -1., -1.7, .15])

    def terms(self, x):
        dx, dy = (np.asarray(x) - self.centers).T
        v = self.amplitudes * np.exp(self.a*dx**2 + self.b*dx*dy + self.c*dy**2)
        return dx, dy, v

    def energy(self, x):
        return float(self.terms(x)[2].sum())

    def force(self, x):
        dx, dy, v = self.terms(x)
        return -np.array([np.sum(v*(2*self.a*dx+self.b*dy)),
                          np.sum(v*(self.b*dx+2*self.c*dy))])

@dataclass
class DoubleWell:
    barrier: float = .15
    coupling: float = 2.

    def energy(self, x):
        x = np.atleast_1d(x)
        value = self.barrier * (x[0]**2 - 1)**2
        if len(x) == 2:
            value += .5 * self.coupling * (1 + x[0]**2) * x[1]**2
        return float(value)

    def force(self, x):
        x = np.atleast_1d(x)
        f = [-4*self.barrier*x[0]*(x[0]**2-1)]
        if len(x) == 2:
            f[0] -= self.coupling*x[0]*x[1]**2
            f.append(-self.coupling*(1+x[0]**2)*x[1])
        return np.array(f)

class LennardJones:
    """Finite nonperiodic cluster in reduced units; no cutoff discontinuity."""
    def energy(self, x):
        x = np.asarray(x).reshape(-1, 3)
        e = 0.
        for i in range(len(x)):
            for j in range(i):
                r2 = np.sum((x[i]-x[j])**2)
                if r2 <= 0:
                    raise ValueError('Coincident particles')
                q = r2**-3
                e += 4*(q*q-q)
        return float(e)

    def force(self, x):
        shape = np.shape(x)
        x = np.asarray(x).reshape(-1, 3)
        f = np.zeros_like(x)
        for i in range(len(x)):
            for j in range(i):
                d = x[i]-x[j]
                r2 = d@d
                if r2 <= 0:
                    raise ValueError('Coincident particles')
                q = r2**-3
                pair = 24*(2*q*q-q)/r2*d
                f[i] += pair
                f[j] -= pair
        return f.reshape(shape)

def finite_force(potential, x, step=1e-5):
    if step <= 0:
        raise ValueError('step must be positive')
    x = np.asarray(x, dtype=float)
    result = np.empty(x.size)
    for i in range(x.size):
        d = np.zeros(x.size)
        d[i] = step
        d = d.reshape(x.shape)
        result[i] = -(potential.energy(x+d)-potential.energy(x-d))/(2*step)
    return result.reshape(x.shape)
