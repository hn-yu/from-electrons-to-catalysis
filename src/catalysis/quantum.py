"""Small reference calculations with explicit basis, spin and convergence records."""
import numpy as np


def hf_failures(config):
    from pyscf import gto, scf
    rows = []
    for index,r in enumerate(config['bond_lengths_A']):
        mol = gto.M(atom=config.get('geometries',[f'H 0 0 0; H 0 0 {v}' for v in config['bond_lengths_A']])[index], basis='sto-3g', verbose=0)
        rhf = scf.RHF(mol).run(conv_tol=1e-10)
        # Deliberately break alpha/beta spatial symmetry; a symmetric start stays RHF-like.
        uhf = scf.UHF(mol)
        dm = np.zeros((2,mol.nao_nr(),mol.nao_nr())); dm[0,0,0] = 1; dm[1,1,1] = 1
        uhf.kernel(dm0=dm)
        rows.append({'r_A':r, 'RHF_Hartree':rhf.e_tot, 'UHF_Hartree':uhf.e_tot,
                     'UHF_S2':float(uhf.spin_square()[0]), 'converged':bool(rhf.converged and uhf.converged)})
    oxygen = []
    for spin in [0,2]:
        mol = gto.M(atom=config.get('oxygen_geometry','O 0 0 0; O 0 0 1.21'), basis='sto-3g', spin=spin, verbose=0)
        mf = scf.UHF(mol).run()
        oxygen.append({'spin_2S':spin, 'energy_Hartree':mf.e_tot, 'S2':float(mf.spin_square()[0]), 'converged':bool(mf.converged)})
    basis = []
    for name in config['bases']:
        mol = gto.M(atom=config.get('geometries',['H 0 0 0; H 0 0 .74'])[0], basis=name, verbose=0)
        mf = scf.RHF(mol).run(conv_tol=1e-10)
        basis.append({'basis':name, 'energy_Hartree':mf.e_tot, 'converged':bool(mf.converged)})
    if not all(r['converged'] for r in rows+oxygen+basis):
        raise RuntimeError('An HF reference failed SCF convergence')
    return {'stretch':rows, 'oxygen':oxygen, 'basis_sweep':basis}


def dft_comparison(config):
    from pyscf import gto, scf, dft, fci
    results = []
    for index,r in enumerate(config['bond_lengths_A']):
        mol = gto.M(atom=config.get('geometries',[f'H 0 0 0; H 0 0 {v}' for v in config['bond_lengths_A']])[index], basis=config['basis'], verbose=0)
        hf = scf.RHF(mol).run(conv_tol=1e-10)
        reference = fci.FCI(hf).kernel()[0]
        row = {'r_A':r, 'HF_Hartree':hf.e_tot, 'FCI_Hartree':reference}
        for xc in ['lda,vwn', 'pbe', 'b3lyp']:
            mf = dft.RKS(mol); mf.xc = xc; mf.grids.level = 3; mf.conv_tol = 1e-9
            mf.kernel()
            if not mf.converged:
                raise RuntimeError(f'{xc} failed SCF')
            row[xc+'_Hartree'] = mf.e_tot
        results.append(row)
    return {'basis':config['basis'], 'results':results,
            'reference_scope':'FCI is exact only within the specified finite basis; all DFT runs are spin restricted.'}


def molecular_thermo(config):
    from ase import Atoms
    from ase.thermochemistry import IdealGasThermo
    from pyscf import gto, scf
    from pyscf.hessian import thermo
    from scipy.optimize import minimize
    from .thermo import ideal_gas
    from .units import convert
    rows = []
    for item in config['molecules']:
        symbols = item['symbols']; shape = np.array(item['positions_A']).shape
        def evaluate(flat):
            mol = gto.M(atom=list(zip(symbols, np.asarray(flat).reshape(shape))), basis=config['basis'], verbose=0)
            mf = scf.RHF(mol).run(conv_tol=1e-11)
            if not mf.converged:
                raise RuntimeError('Molecular SCF failed')
            # PySCF gradients are Eh/bohr, scipy coordinates are angstrom.
            return mf.e_tot, mf.nuc_grad_method().kernel().ravel()/0.529177210903
        opt = minimize(evaluate, np.array(item['positions_A']).ravel(), jac=True, method='BFGS',
                       options={'gtol':2e-5, 'maxiter':150})
        if np.max(abs(opt.jac)) > 5e-5:
            raise RuntimeError(f"Geometry not stationary: {item['name']}")
        positions = opt.x.reshape(shape)
        mol = gto.M(atom=list(zip(symbols, positions)), basis=config['basis'], verbose=0)
        mf = scf.RHF(mol).run(conv_tol=1e-11)
        vib = thermo.harmonic_analysis(mol, mf.Hessian().kernel())
        frequencies = np.asarray(vib['freq_wavenumber'])
        if np.max(abs(frequencies.imag)) > 1e-6 or np.any(frequencies.real <= 0):
            raise RuntimeError('Imaginary/nonpositive internal vibrational frequency')
        quanta = convert(frequencies.real, 'cm^-1','eV')
        atoms = Atoms(symbols, positions=positions)
        electronic = float(convert(mf.e_tot,'Hartree','eV'))
        ours = ideal_gas(atoms, quanta, config['temperature_K'], config['pressure_bar'],
                         item['symmetry'], electronic, spin=item.get('spin',0), linear=item['linear'])
        ref = IdealGasThermo(vib_energies=quanta, potentialenergy=electronic,
                             atoms=atoms, geometry='linear' if item['linear'] else 'nonlinear',
                             symmetrynumber=item['symmetry'], spin=item.get('spin',0))
        gref = ref.get_gibbs_energy(config['temperature_K'],config['pressure_bar']*1e5,verbose=False)
        rows.append({'molecule':item['name'], 'positions_A':positions.tolist(),
                     'frequencies_cm^-1':frequencies.real.tolist(), **ours,
                     'ASE_G_eV':float(gref), 'G_error_eV':float(ours['G_eV']-gref),
                     'gradient_max_Hartree_A':float(np.max(abs(opt.jac)))})
    return {'method':'RHF/'+config['basis']+' optimized geometry and analytic Hessian; ideal-gas RRHO', 'results':rows}
