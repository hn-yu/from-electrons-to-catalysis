"""Crawford-style indexed AO integral tables, independent of any SCF package."""
from pathlib import Path
import numpy as np


def load_integrals(folder):
    folder=Path(folder)
    norb,nelectron,enuc=np.loadtxt(folder/'system.dat')
    norb,nelectron=int(norb),int(nelectron)
    matrices=[]
    for name in ['s','t','v']:
        matrix=np.zeros((norb,norb))
        for i,j,value in np.atleast_2d(np.loadtxt(folder/f'{name}.dat')):
            i,j=int(i)-1,int(j)-1
            if not (0<=i<norb and 0<=j<norb):raise ValueError('AO index out of bounds')
            matrix[i,j]=matrix[j,i]=value
        matrices.append(matrix)
    eri=np.zeros((norb,)*4)
    for i,j,k,l,value in np.atleast_2d(np.loadtxt(folder/'eri.dat')):
        i,j,k,l=(int(x)-1 for x in (i,j,k,l))
        if not all(0<=x<norb for x in (i,j,k,l)):raise ValueError('ERI index out of bounds')
        for a,b in [(i,j),(j,i)]:
            for c,d in [(k,l),(l,k)]:
                eri[a,b,c,d]=eri[c,d,a,b]=value
    s,t,v=matrices
    return s,t+v,eri,nelectron,float(enuc)


def export_integrals(mol,folder):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    n=mol.nao_nr()
    np.savetxt(folder/'system.dat',[[n,mol.nelectron,mol.energy_nuc()]],fmt=['%d','%d','%.16e'],header='nAO nElectron Enuc_Hartree')
    for file,integral in [('s','int1e_ovlp'),('t','int1e_kin'),('v','int1e_nuc')]:
        matrix=mol.intor(integral)
        rows=[[i+1,j+1,matrix[i,j]] for i in range(n) for j in range(i+1)]
        np.savetxt(folder/f'{file}.dat',rows,fmt=['%d','%d','%.16e'],header='i j value; 1-based lower triangle; S dimensionless, T/V Hartree')
    eri=mol.intor('int2e');pairs=[(i,j) for i in range(n) for j in range(i+1)];rows=[]
    for p,(i,j) in enumerate(pairs):
        for k,l in pairs[:p+1]:
            if abs(eri[i,j,k,l])>1e-14:rows.append([i+1,j+1,k+1,l+1,eri[i,j,k,l]])
    np.savetxt(folder/'eri.dat',rows,fmt=['%d']*4+['%.16e'],header='i j k l (ij|kl)_Hartree; unique nonzero AO ERIs, 1-based')
