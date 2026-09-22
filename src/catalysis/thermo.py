"""Canonical statistics and ideal-gas rigid-rotor/harmonic-oscillator thermochemistry."""
import numpy as np
from scipy.special import logsumexp
from .units import KB, H, EV_J, AMU_KG, kbt


def partition(energies, temperature, degeneracies=None):
    e = np.asarray(energies, dtype=float)
    g = np.ones_like(e) if degeneracies is None else np.asarray(degeneracies, dtype=float)
    if e.ndim != 1 or len(e) == 0 or g.shape != e.shape or np.any(g <= 0):
        raise ValueError('Provide energies and positive matching degeneracies')
    kt = float(kbt(temperature))
    logweights = np.log(g)-e/kt
    logz = logsumexp(logweights)
    p = np.exp(logweights-logz)
    u = float(p@e)
    f = -kt*logz
    return {'logZ': float(logz), 'populations': p.tolist(), 'U_eV': u,
            'F_eV': float(f), 'S_eV_K': float((u-f)/temperature)}


def oscillator(quanta, temperature):
    q = np.atleast_1d(quanta).astype(float)
    if np.any(q <= 0):
        raise ValueError('Vibrational quanta must be positive; remove rigid modes first')
    kt = float(kbt(temperature))
    x = q/kt
    logthermal = np.log(-np.expm1(-x))
    occupation = np.exp(-x)/(-np.expm1(-x))
    zpe = .5*q.sum()
    u = zpe+np.sum(q*occupation)
    f = zpe+kt*logthermal.sum()
    return {'ZPE_eV': float(zpe), 'U_eV': float(u), 'F_eV': float(f),
            'S_eV_K': float((u-f)/temperature)}


def chemical_potential(mu0, temperature, pressure_bar, standard_bar=1.):
    if np.any(np.asarray(pressure_bar) <= 0) or standard_bar <= 0:
        raise ValueError('Pressures must be positive')
    return mu0+kbt(temperature)*np.log(np.asarray(pressure_bar)/standard_bar)


def ideal_gas(atoms, quanta, temperature, pressure_bar=1., symmetry=1,
              electronic_energy=0., spin=0., linear=False):
    """RRHO per molecule, high-T rotor, ideal translation, electronic degeneracy 2S+1."""
    if pressure_bar <= 0 or symmetry <= 0 or spin < 0:
        raise ValueError('Invalid pressure, symmetry or spin')
    t = temperature; kt = float(kbt(t)); ktj = kt*EV_J; hj = H*EV_J
    mass = atoms.get_masses().sum()*AMU_KG
    qtrans = (2*np.pi*mass*ktj/hj**2)**1.5 * ktj/(pressure_bar*1e5)
    moments = atoms.get_moments_of_inertia()*AMU_KG*1e-20
    if linear:
        qrot = 8*np.pi**2*max(moments)*ktj/(symmetry*hj**2)
        rot_dof = 1.
    else:
        if np.min(moments) <= 0:
            raise ValueError('Nonlinear rotor requires three positive moments')
        qrot = np.sqrt(np.pi)*np.sqrt(np.prod(8*np.pi**2*moments*ktj/hj**2))/symmetry
        rot_dof = 1.5
    vib = oscillator(quanta, t)
    entropy = KB*(np.log(qtrans)+2.5+np.log(qrot)+rot_dof+np.log(2*spin+1))+vib['S_eV_K']
    enthalpy = electronic_energy+(2.5+rot_dof)*kt+vib['U_eV']
    return {'electronic_eV': electronic_energy, 'ZPE_eV': vib['ZPE_eV'],
            'thermal_enthalpy_eV': enthalpy-electronic_energy-vib['ZPE_eV'],
            'H_eV': float(enthalpy), 'S_eV_K': float(entropy), 'G_eV': float(enthalpy-t*entropy)}


def surface_phase(states, chemical_potentials):
    """Relative grand potentials for equal-area, one-sided surface cells."""
    mu = np.asarray(chemical_potentials)
    omega = np.array([s['energy_eV']-s['adsorbates']*mu for s in states])
    winners = np.argmin(omega, axis=0)
    return {'mu_eV': mu.tolist(), 'grand_potential_eV': omega.tolist(),
            'stable_state': [states[i]['name'] for i in winners]}
