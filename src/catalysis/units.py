"""CODATA/SI conversions. Each conversion is multiplicative and dimension checked."""
import numpy as np
KB = 8.617333262145e-5  # eV / K
H = 4.135667696e-15  # eV s
EV_J = 1.602176634e-19
AMU_KG = 1.66053906660e-27
HBAR = H / (2 * np.pi)
_GROUPS = {
    'energy': {'eV': 1., 'kJ/mol': 1 / 96.4853321233, 'Hartree': 27.211386245988,
               'cm^-1': 1.239841984332e-4},
    'pressure': {'Pa': 1., 'bar': 1e5},
    'time': {'s': 1., 'ms': 1e-3, 'us': 1e-6, 'ns': 1e-9, 'ps': 1e-12, 'fs': 1e-15},
}

def convert(value, source, target):
    for units in _GROUPS.values():
        if source in units and target in units:
            return np.asarray(value) * units[source] / units[target]
    raise ValueError(f'Incompatible or unknown units: {source}, {target}')

def kbt(temperature):
    t = np.asarray(temperature, dtype=float)
    if np.any(t <= 0):
        raise ValueError('Temperature must be positive (K)')
    return KB * t
