"""Finite grids, nonorthogonal bases and a hand-written restricted SCF loop."""
import numpy as np
from scipy.linalg import eigh, eigh_tridiagonal


def schrodinger(kind='harmonic', n=400, length=12., states=4):
    if n < states or length <= 0:
        raise ValueError('Need n >= states and positive length')
    # Interior points; Dirichlet walls at ±length/2; atomic units.
    dx = length/(n+1)
    x = np.linspace(-length/2+dx, length/2-dx, n)
    potentials = {'box': np.zeros(n), 'harmonic': .5*x*x,
                  'finite_well': np.where(abs(x)<1, -5., 0.),
                  'double_well': .1*(x*x-4)**2}
    v = potentials[kind]
    e, psi = eigh_tridiagonal(1/dx**2+v, np.full(n-1, -.5/dx**2),
                              select='i', select_range=(0, states-1))
    return x, e, psi/np.sqrt(dx)


def lcao(h, s):
    h, s = np.asarray(h), np.asarray(s)
    if np.linalg.eigvalsh(s).min() <= 1e-10:
        raise ValueError('Overlap is not positive definite')
    return eigh(h, s)


def rhf(atom, basis='sto-3g', charge=0, tolerance=1e-9, maxiter=200):
    from pyscf import gto, scf
    mol = gto.M(atom=atom, basis=basis, charge=charge, spin=0, verbose=0)
    if mol.nelectron % 2:
        raise ValueError('RHF requires an even electron count')
    overlap = mol.intor('int1e_ovlp')
    core = mol.intor('int1e_kin')+mol.intor('int1e_nuc')
    eri = mol.intor('int2e')
    w, u = eigh(overlap)
    if w.min() < 1e-10:
        raise ValueError('Linearly dependent AO basis')
    x = (u / np.sqrt(w)) @ u.T
    nocc = mol.nelectron//2
    def density(fock):
        _, c = eigh(x.T@fock@x)
        c = x@c[:, :nocc]
        return 2*c@c.T
    def fock(p):
        j = np.einsum('pqrs,rs->pq', eri, p)
        k = np.einsum('prqs,rs->pq', eri, p)
        return core+j-.5*k
    p = density(core)
    history, fs, errors = [], [], []
    old = np.inf
    for iteration in range(1, maxiter+1):
        f = fock(p)
        residual = x.T@(f@p@overlap-overlap@p@f)@x
        fs.append(f.copy()); errors.append(residual.ravel())
        fs, errors = fs[-7:], errors[-7:]
        if len(fs) > 1:
            m = len(fs)
            b = np.empty((m+1, m+1)); b[:m,:m] = np.array(errors)@np.array(errors).T
            b[m,:] = -1; b[:,m] = -1; b[m,m] = 0
            rhs = np.zeros(m+1); rhs[m] = -1
            try:
                coeff = np.linalg.solve(b, rhs)[:m]
                f = np.einsum('i,ijk->jk', coeff, np.array(fs))
            except np.linalg.LinAlgError:
                pass
        new = density(f)
        fnew = fock(new)
        energy = .5*np.sum(new*(core+fnew))+mol.energy_nuc()
        dp = np.linalg.norm(new-p)
        residual_norm = np.linalg.norm(x.T@(fnew@new@overlap-overlap@new@fnew)@x)
        history.append([iteration, float(energy), float(dp), float(residual_norm)])
        if abs(energy-old) < tolerance and dp < np.sqrt(tolerance) and residual_norm < np.sqrt(tolerance):
            p = new
            break
        p, old = new, energy
    else:
        raise RuntimeError('RHF did not converge')
    reference = scf.RHF(mol).run(conv_tol=tolerance*.1).e_tot
    return {'energy_Hartree': float(energy), 'reference_Hartree': float(reference),
            'error_Hartree': float(energy-reference), 'electrons': float(np.trace(p@overlap)),
            'iterations': iteration, 'history': history}
