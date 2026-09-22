"""Sample explicit umbrella windows, then compare own WHAM with PyMBAR FES."""
from pathlib import Path
import numpy as np
from pymbar import FES
from catalysis import sampling
from catalysis.teaching_io import arguments,controls,table,write_table,record,summary
from catalysis.units import kbt
args=arguments(Path(__file__).parent);c=controls(args.input)
windows=table(args.input/'windows.csv');centers=np.array([float(r['center']) for r in windows])
kappas=np.array([float(r['kappa_eV']) for r in windows]);kt=float(kbt(c['temperature']))
result={}
for dimensions,name in [(1,'one_dimension'),(2,'hidden_coordinate')]:
    folder=args.output/name
    own=sampling.umbrella(**c,dimensions=dimensions,centers=centers,kappas=kappas,trajectory_dir=folder)
    samples=[np.loadtxt(folder/f'window-{i:02}.csv',delimiter=',',skiprows=1) for i in range(len(centers))]
    xy=np.concatenate(samples);x,y=xy.T
    potential=.15*(x*x-1)**2+(1+x*x)*y*y
    u_kn=(potential[None,:]+.5*kappas[:,None]*(x[None,:]-centers[:,None])**2)/kt
    fes=FES(u_kn,np.array([len(v) for v in samples]),mbar_options={'relative_tolerance':1e-10})
    edges=np.linspace(-1.8,1.8,121);bins=(edges[1:]+edges[:-1])/2
    fes.generate_fes(potential/kt,x,histogram_parameters={'bin_edges':[edges]})
    counts=np.array(own['counts']).sum(axis=0);mask=counts>0
    reference=np.full(len(bins),np.nan);reference[mask]=kt*fes.get_fes(bins[mask],reference_point='from-lowest')['f_i']
    manual=np.array([np.nan if v is None else v for v in own['F_eV']])
    selected=(abs(bins)<1.3)&(counts>30)
    delta=manual[selected]-reference[selected];delta-=delta.mean()
    own['PyMBAR_shape_RMSE_eV']=float(np.sqrt(np.mean(delta**2)))
    write_table(folder/'F-comparison.csv',['x_model','own_WHAM_eV','PyMBAR_FES_eV','analytic_eV','samples'],zip(bins,manual,reference,own['exact_F_eV'],counts))
    write_table(folder/'window-diagnostics.csv',['window','center','acceptance','mean_y'],zip(range(len(centers)),centers,own['acceptance'],own['hidden_means']))
    result[name]=own
result['bad_coordinate']=sampling.bad_coordinate(c['temperature'],c['seed'])
record(args,result,'\n'.join(summary(result))+'\nF-comparison.csv compares binned WHAM with unbinned MBAR weights.\nTrajectories are correlated: no independent-sample uncertainty is claimed.')
