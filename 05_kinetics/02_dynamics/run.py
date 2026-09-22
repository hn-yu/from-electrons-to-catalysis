"""Read scientific input files, execute the stated method, and report observables."""
from pathlib import Path
import numpy as np
from catalysis.teaching_io import arguments, controls, table, column, write_table, record, summary, read_xyz, atom_string
args = arguments(Path(__file__).parent)
c = controls(args.input)
from ase.io import read,write
from ase.calculators.calculator import Calculator,all_changes
from ase.md.verlet import VelocityVerlet
from catalysis.kinetics import verlet
from catalysis.potentials import Harmonic,LennardJones
from ase import units
rows=[]
for dt in column(args.input/'timesteps.csv','dt_reduced'):
    trajectory=verlet(Harmonic(),[1.],[0.],dt,c['steps'])
    rows.append({'dt_reduced':dt,'max_energy_error':float(np.max(abs(trajectory[:,1]-.5)))})
atoms=read(args.input/'cluster.extxyz');p=LennardJones();dt=.002;steps=2000
# Identical forces isolate the integrator comparison. Units here are ASE internal units.
class Cluster(Calculator):
    implemented_properties=['energy','forces']
    def calculate(self,atoms=None,properties=('energy',),system_changes=all_changes):
        super().calculate(atoms,properties,system_changes)
        self.results={'energy':p.energy(self.atoms.positions),'forces':p.force(self.atoms.positions)}
own=verlet(p,atoms.positions,atoms.get_velocities(),dt,steps,mass=atoms.get_masses()[:,None])
atoms.calc=Cluster();reference=[]
dyn=VelocityVerlet(atoms,dt,logfile=None)
def collect():reference.append([dyn.nsteps*dt,atoms.get_total_energy(),*atoms.positions.ravel()])
dyn.attach(collect,interval=1);dyn.run(steps);reference=np.array(reference)
write_table(args.output/'own-Verlet.csv',['time_internal','E_eV','x1','y1','z1','x2','y2','z2'],own)
write_table(args.output/'ASE-Verlet.csv',['time_internal','E_eV','x1','y1','z1','x2','y2','z2'],reference)
write(args.output/'final.extxyz',atoms)
result={'timestep_sweep':rows,'dt_fs':dt/units.fs,'max_position_difference_A':float(np.max(abs(own[:,2:]-reference[:,2:]))),
        'max_energy_difference_eV':float(np.max(abs(own[:,1]-reference[:,1]))),'cluster_energy_span_eV':float(np.ptp(own[:,1])),
        'scope':'LJ epsilon=1 eV sigma=1 A mass=1 u model; Ar labels do not imply physical argon parameters.'}

from catalysis.teaching_io import export_tables
export_tables(args.output, result)
record(args, result, '\n'.join(summary(result)) + '\nTables and arrays are saved alongside this report.')
