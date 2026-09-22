"""Render scientific figures from native tables; never generate or overwrite analysis prose."""
from pathlib import Path
import csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
plt.rcParams.update({'figure.figsize':(6.5,4.2),'axes.grid':True,'grid.alpha':.2,'svg.hashsalt':'native-course'})


def numeric(path):return np.loadtxt(path,delimiter=',',skiprows=1,ndmin=2)
def save(folder,name='figure.svg'):
    plt.tight_layout();path=folder/name
    plt.savefig(path,metadata={'Date':None});plt.close()
    path.write_text('\n'.join(line.rstrip() for line in path.read_text().splitlines())+'\n')

folder=ROOT/'02_bringup/02_forces/output';a=numeric(folder/'scan.csv')
plt.plot(a[:,0],a[:,3],'o-',label='Own analytic');plt.plot(a[:,0],a[:,4],'x',label='ASE');plt.plot(a[:,0],a[:,5],'.',label='Finite difference')
plt.xlabel('Bond distance (A)');plt.ylabel('Radial force (eV/A)');plt.legend();save(folder)
folder=ROOT/'02_bringup/03_finite_differences/output';a=numeric(folder/'scan.csv')
plt.loglog(a[:,0],a[:,1],'o-');plt.xlabel('Displacement h (A)');plt.ylabel('Absolute force error (eV/A)');save(folder)
folder=ROOT/'03_electronic_structure/03_rhf/output'
for case in ['HeHplus','LiH','H2O']:
    a=numeric(folder/case/'iterations.csv');plt.semilogy(a[:,0],a[:,3],'.-',label=case)
plt.xlabel('SCF iteration');plt.ylabel('Commutator norm');plt.legend();save(folder)

def records(path):
    with path.open() as f:return list(csv.DictReader(f))
def values(rows,key):return np.array([float(row[key]) for row in rows])
folder=ROOT/'03_electronic_structure/04_break_hf/output';rows=records(folder/'stretch.csv')
for key in ['RHF_Hartree','UHF_Hartree']:plt.plot(values(rows,'r_A'),values(rows,key),'o-',label=key.split('_')[0])
plt.xlabel('H-H distance (A)');plt.ylabel('Energy (Hartree)');plt.legend();save(folder)
folder=ROOT/'03_electronic_structure/06_periodic/output';rows=records(folder.parent/'input/eos.csv')
for scenario in dict.fromkeys(r['scenario'] for r in rows):
    selected=[r for r in rows if r['scenario']==scenario];e=values(selected,'energy_eV_atom')
    plt.plot(values(selected,'volume_A3_atom'),e-e.min(),'o-',label=scenario)
plt.xlabel('Volume (A^3/atom)');plt.ylabel('E - sampled minimum (eV/atom)');plt.legend(fontsize=8);save(folder)
folder=ROOT/'04_thermodynamics/01_partition/output';rows=records(folder/'two_level.csv')
plt.semilogx(values(rows,'T_K'),values(rows,'U_eV'),'o-',label='U');plt.semilogx(values(rows,'T_K'),values(rows,'F_eV'),'o-',label='F')
plt.xlabel('Temperature (K)');plt.ylabel('Energy (eV)');plt.legend();save(folder)
folder=ROOT/'05_kinetics/02_dynamics/output';a=numeric(folder/'own-Verlet.csv');b=numeric(folder/'ASE-Verlet.csv')
plt.plot(a[:,0],a[:,1]-a[0,1],label='Own');plt.plot(b[:,0],b[:,1]-b[0,1],'--',label='ASE')
plt.xlabel('Time (ASE internal units)');plt.ylabel('E(t) - E(0) (eV)');plt.legend();save(folder)
folder=ROOT/'05_kinetics/03_hessian/output';a=numeric(folder/'normal_modes.csv')
plt.plot(a[:,0],a[:,2],'o',label='Own mass weighting');plt.plot(a[:,0],a[:,3],'x',label='ASE')
plt.xlabel('Mode');plt.ylabel('Signed frequency (cm^-1)');plt.legend();save(folder)
folder=ROOT/'05_kinetics/04_neb/output';a=numeric(folder/'own-band.csv');distance=np.r_[0,np.cumsum(np.linalg.norm(np.diff(a[:,:2],axis=0),axis=1))]
plt.plot(distance,a[:,2]-a[0,2],'o-');plt.xlabel('Path length (model units)');plt.ylabel('Energy relative to initial state (eV)');save(folder)
folder=ROOT/'06_catalysis/03_umbrella/output'
for name in ['one_dimension','hidden_coordinate']:
    a=numeric(folder/name/'F-comparison.csv')
    plt.plot(a[:,0],a[:,1],label='Own WHAM');plt.plot(a[:,0],a[:,2],'--',label='PyMBAR');plt.plot(a[:,0],a[:,3],':',label='Analytic')
    plt.xlim(-1.35,1.35);plt.ylim(0,.2);plt.xlabel('x (model coordinate)');plt.ylabel('F - minimum (eV)');plt.legend();save(folder,name+'.svg')
for project in ['06_catalysis/01_slab','07_real_system/02_real_dft']:
    folder=ROOT/project/'output';rows=records(folder/'sweep.csv')
    labels=[f"{r['parameter']}={r['value']}" for r in rows];plt.barh(labels,values(rows,'delta_from_baseline_eV'))
    plt.axvline(.05,color='r',ls='--');plt.axvline(-.05,color='r',ls='--');plt.xlabel('Change in adsorption energy (eV)');save(folder)
folder=ROOT/'06_catalysis/02_adsorption/output';rows=records(folder/'sites.csv')
plt.bar([r['initial_site'] for r in rows],values(rows,'adsorption_eV'));plt.ylabel('PBE adsorption energy (eV/H)');save(folder)
