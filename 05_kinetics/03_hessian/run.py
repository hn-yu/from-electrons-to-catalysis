"""Cartesian Hessian text → manual mass weighting → ASE vibrational reference."""
from pathlib import Path
import numpy as np
from ase.vibrations import VibrationsData
from ase import units as ase_units
from catalysis.teaching_io import arguments,controls,read_xyz,record,write_table
from catalysis.kinetics import hessian,minimize
from catalysis.potentials import Morse,MullerBrown
from scipy.optimize import root


def main():
    args=arguments(Path(__file__).parent)
    config=controls(args.input)
    atoms=read_xyz(args.input/'H2O_optimized.xyz')
    mass=np.loadtxt(args.input/'masses.dat')
    raw=np.loadtxt(args.input/'hessian.dat')
    if raw.shape!=(3*len(atoms),)*2 or mass.shape!=(len(atoms),):raise ValueError('Geometry/Hessian/mass dimensions disagree')
    if np.any(mass<=0):raise ValueError("Masses must be positive")
    atoms.set_masses(mass)
    # Convert Eh/bohr² to eV/Å² before comparing with ASE.
    h_cart=raw*ase_units.Hartree/ase_units.Bohr**2
    expanded=np.repeat(mass,3)
    h_mw=h_cart/np.sqrt(expanded[:,None]*expanded[None,:])
    eig,modes=np.linalg.eigh((h_mw+h_mw.T)/2)
    # sqrt(eV/Å²/u) → angular frequency (s^-1), then wavenumber.
    factor=np.sqrt(1.602176634e-19/(1e-20*1.66053906660e-27))/(2*np.pi*2.99792458e10)
    frequencies=np.sign(eig)*np.sqrt(abs(eig))*factor
    ase_freq=VibrationsData.from_2d(atoms,h_cart).get_frequencies()
    ase_signed=np.where(abs(ase_freq.imag)>1e-8,-abs(ase_freq.imag),ase_freq.real)
    rows=[[i+1,eig[i],frequencies[i],float(ase_signed[i])] for i in range(len(eig))]
    write_table(args.output/'normal_modes.csv',['mode','lambda_eV_A2_u','own_cm^-1','ASE_signed_cm^-1'],rows)
    np.savetxt(args.output/'mass_weighted_hessian.dat',h_mw,header='eV / (A^2 u)')
    np.savetxt(args.output/'eigenvectors.dat',modes,header='mass-weighted eigenvectors are columns')
    # Retain the force-difference exercise; the molecular matrix checks its downstream analysis.
    hm,values,_=hessian(Morse(),[.74],mass=config['morse_mass_amu'])
    guesses=np.loadtxt(args.input/'stationary_guesses.dat')
    minimum=minimize(MullerBrown(),guesses[0])
    _,minimum_curvature,_=hessian(MullerBrown(),minimum['x'])
    saddle=root(lambda x:MullerBrown().force(x),guesses[1])
    if not saddle.success:raise RuntimeError('Toy saddle failed')
    _,curvature,_=hessian(MullerBrown(),saddle.x)
    result={'molecule':'H2O','frequencies_cm^-1':frequencies.tolist(),'ASE_signed_cm^-1':ase_signed.tolist(),
            'frequency_error_max_cm^-1':float(np.max(abs(frequencies-ase_signed))),
            'morse_curvature':float(hm[0,0]),'morse_mass_weighted_curvature':float(values[0]),
            'toy_minimum_negative_modes':int(sum(minimum_curvature<0)),'toy_saddle_negative_modes':int(sum(curvature<0))}
    lines=['H2O Cartesian Hessian analysis','input: Hartree/bohr^2; mass: u',
           'mode lambda[eV/(A^2 u)] own[cm^-1] ASE[cm^-1]']
    lines += ['%2d % .8e %12.5f %12.5f'%tuple(row) for row in rows]
    lines += ['Six near-zero rigid modes are expected for nonlinear H2O.',
              'A negative sign denotes an imaginary mode; never take abs() and call it stable.']
    record(args,result,'\n'.join(lines))

if __name__=='__main__':main()
