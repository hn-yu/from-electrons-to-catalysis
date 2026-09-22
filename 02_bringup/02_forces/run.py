"""Read scientific input files, execute the stated method, and report observables."""
from pathlib import Path
import numpy as np
from catalysis.teaching_io import arguments, controls, table, column, write_table, record, summary, read_xyz, atom_string
args = arguments(Path(__file__).parent)
c = controls(args.input)
from ase.io import read
from ase.calculators.morse import MorsePotential
from catalysis.potentials import Morse, finite_force
p=Morse(**c['potential']); rows=[];cartesian=[]
for atoms in read(args.input/c['geometry'],index=':'):
    r=atoms.get_distance(0,1); direction=(atoms.positions[1]-atoms.positions[0])/r
    atoms.calc=MorsePotential(epsilon=p.depth,r0=p.equilibrium,rho0=p.alpha*p.equilibrium,rcut1=100,rcut2=101)
    force=float(p.force(r)); library_forces=atoms.get_forces();reference=float(library_forces[1]@direction)
    own_forces=np.array([-force*direction,force*direction])
    for i in range(2):cartesian.append([len(rows),i,*atoms.positions[i],*own_forces[i],*library_forces[i]])
    rows.append([r,p.energy(r),atoms.get_potential_energy(),force,reference,float(finite_force(p,r,c['step_A']))])
write_table(args.output/'Cartesian-forces.csv',['frame','atom','x_A','y_A','z_A','own_Fx','own_Fy','own_Fz','ASE_Fx','ASE_Fy','ASE_Fz'],cartesian)
result={'Cartesian_force_max_error_eV_A':float(np.max(abs(np.array(cartesian)[:,5:8]-np.array(cartesian)[:,8:11]))),'columns':['r_A','own_E_eV','ASE_E_eV','own_radial_F_eV_A','ASE_radial_F_eV_A','FD_radial_F_eV_A'],
        'scan':rows,'max_ASE_force_error':float(np.max(abs(np.array(rows)[:,3]-np.array(rows)[:,4])))}

from catalysis.teaching_io import export_tables
export_tables(args.output, result)
record(args, result, '\n'.join(summary(result)) + '\nTables and arrays are saved alongside this report.')
