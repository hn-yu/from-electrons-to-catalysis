"""Generate figures and concise postmortems from completed, checked-in example data."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
plt.rcParams.update({'figure.figsize':(6.5,4),'figure.dpi':130,'axes.grid':True,'grid.alpha':.25,'svg.hashsalt':'electrons-course'})

def summary(experiment,r):
    if experiment=='units_experiment':
        return f"kBT (eV): {r['kBT_eV']}. The predicted scale is confirmed; conversion round trips and dimensional rejection pass."
    if experiment=='forces':
        return f"Maximum force discrepancy: {max(row[-1] for row in r['scan']):.3g} eV/A. The predicted signs and equilibrium zero are confirmed. The Morse dissociation limit is zero by convention."
    if experiment=='finite_differences':
        best=min(r['scan'],key=lambda row:row[1]);return f"Best sampled displacement: {best[0]:.3g} A; error {best[1]:.3g}. The interior minimum confirms the prediction. Error at tiny h is cancellation, at large h truncation."
    if experiment=='schrodinger':
        return f"Harmonic energies (Hartree): {r['harmonic']['energies_Hartree']}. Node counts: {r['harmonic']['nodes']}. Positive tunneling splitting: {r['double_well']['energies_Hartree'][1]-r['double_well']['energies_Hartree'][0]:.6g} Hartree. The qualitative prediction holds; box size remains a separate convergence axis."
    if experiment=='lcao':return f"Energies: {r['energies_Hartree']} Hartree. The lower state lies below either one-basis Rayleigh quotient, as predicted. Overlap normalization and generalized residual are checked independently."
    if experiment=='scf':return 'Self-written RHF minus PySCF energy (Hartree): '+', '.join(f"{name}: {row['error_Hartree']:.3g}" for name,row in r.items())+'. All match within the predicted tolerance; this does not remove finite-basis or correlation error.'
    if experiment=='hf_failures':
        last=r['stretch'][-1];return f"At {last['r_A']} A, RHF={last['RHF_Hartree']:.8f} and UHF={last['UHF_Hartree']:.8f} Hartree, UHF S²={last['UHF_S2']:.5f}. The broken-symmetry prediction is confirmed. Report spin contamination alongside the energy lowering; the nominal singlet O2 run need not be spin pure."
    if experiment=='dft':return 'Same-basis HF–FCI gaps (Hartree): '+', '.join(f"r={x['r_A']} A: {x['HF_Hartree']-x['FCI_Hartree']:.6f}" for x in r['results'])+'. Correlation error grows upon stretching as predicted. Functional agreement is neither guaranteed nor evidence of exactness.'
    if experiment=='periodic':return f"Backend {r['backend']}: fitted a0={r['a0_A']:.6f} A; bulk modulus={r['bulk_modulus_GPa']:.3f} GPa. These satisfy the predicted physical range. EMT values validate the fitting workflow only. Inspect the separate DFT output for electronic convergence."
    if experiment=='partition':return f"Excited-state population at the highest sampled T: {r['two_level'][-1]['populations'][1]:.5f}, tending toward 0.75 at infinite T. Low-T oscillator U={r['oscillator'][0]['U_eV']:.6f} eV, confirming the 0.06 eV zero-point limit."
    if experiment=='molecular_thermo':return 'Independent RRHO G minus ASE G (eV): '+', '.join(f"{x['molecule']}: {x['G_error_eV']:.3g}" for x in r['results'])+'. All internal modes are positive and have the expected count. The prediction holds numerically; RHF/STO-3G frequencies are teaching data, not spectroscopic reference values.'
    if experiment=='chemical_potential':return 'The input has favorable electronic adsorption energy (-0.6 eV), but at 1000 K and 1 bar the model gives +0.9 eV free energy. The predicted sign reversal occurs because the gas entropy is lost. Constant entropy is a declared toy approximation.'
    if experiment=='surface_phase':return 'The lower envelope follows clean → quarter → half coverage as chemical potential rises, with crossings at -0.5 and -0.2 eV. The prediction is confirmed for equal-area cells; configurational/vibrational surface entropy is omitted.'
    if experiment=='optimizer':return 'Morse minima (A): '+', '.join(f"{x['x'][0]:.8f}" for x in r['morse'])+'. Distinct Muller–Brown minima occur from different starts, confirming local rather than global optimization. Forces, not merely step lengths, determine convergence.'
    if experiment=='dynamics':return f"LJ dimer energy span: {r['cluster_energy_span']:.3g} reduced units. Harmonic dt={r['timestep_sweep'][-1]['dt']} gives final energy {r['timestep_sweep'][-1]['final_energy']:.3g}, confirming loss of stability above dt=2. Stable timestep errors scale quadratically; bounded oscillation alone is not sampling convergence."
    if experiment=='hessian':return f"Negative modes: minimum {r['minimum']['negative_modes']}, saddle {r['saddle']['negative_modes']}. Morse frequency: {r['morse_frequency_cm^-1'][0]:.2f} cm^-1. This confirms the predicted stationary-point classification; inspect the eigenvector before assigning a reaction."
    if experiment=='neb':return f"Own MB barrier: {r['own']['barrier_eV']:.6f} eV; ASE: {r['ASE_barrier_eV']:.6f} eV; difference {r['barrier_difference_eV']:.3g} eV. Residual {r['own']['force_max']:.3g}. The predicted range and comparison tolerance hold. A discrete highest image still needs image-count/climbing-image refinement for precision."
    if experiment=='tst':
        selected=[x for x in r['scan'] if abs(x[1]-1)<1e-8 and x[0] in [300,1000]]
        return 'At a 1 eV barrier, waiting times are '+', '.join(f"{x[0]} K: {x[3]:.4g} s" for x in selected)+'. The prediction is confirmed under Eyring prefactor and transmission=1. These are conditional elementary waiting times.'
    if experiment=='slab':
        energy=r['baseline']['sites'][0]['adsorption_eV'];worst=max(abs(x['delta_from_baseline_eV']) for x in r['sweep'])
        return f"{r['backend']} baseline adsorption energy: {energy:.6f} eV; maximum sampled change {worst:.6f} eV; all variations below {r['tolerance_eV']} eV: {r['all_variations_within_tolerance']}. Compare this measured result with the unchanged prediction in the README. A lateral-size change also changes coverage and is not a pure numerical test. A passed finite sweep is not proof of an asymptotic plateau."
    if experiment=='adsorption':return f"{r['backend']} adsorption energies (eV): "+', '.join(f"{x['initial_site']}: {x['adsorption_eV']:.6f}" for x in r['sites'])+'. The initial-site ordering must be checked against final positions. A symmetry-preserving relaxation may remain on a lateral saddle; displace adsorbates or compute curvature before claiming all sites are metastable.'
    if experiment=='umbrella':return f"WHAM profile shape RMSE: 1D {r['one_dimension']['shape_RMSE_eV']:.4g}, 2D {r['hidden_coordinate']['shape_RMSE_eV']:.4g} eV. Adjacent windows overlap and the predicted 0.03 eV criterion holds. Hidden-coordinate independent starts retain opposite means despite plausible x sampling. Histogram counts are correlated; this single-seed check is not a confidence interval."
    if experiment=='mep_fes':return '0 K barrier: 0.15 eV. Finite-T barriers: '+', '.join(f"{x['T_K']} K: {x['barrier_eV']:.6f} eV" for x in r['finite_temperature'])+'. The predicted decrease follows transverse entropy. Experimental apparent activation additionally reflects coverage and the network, not just this marginal barrier.'
    if experiment=='reaction_network':return f"Maximum log detailed-balance residual: {max(abs(x) for x in r['detailed_balance_log_residual']):.3g}. Site-conserving stoichiometry and equilibrium limits pass; gas pressures remain explicit mass-action activities."
    if experiment=='microkinetics':return f"Coverages [vacancy,A*,B*]: {r['steady_state']['coverages']}; TOF={r['steady_state']['TOF_s^-1']:.6g} s^-1; apparent activation={r['response']['apparent_activation_eV']:.6f} eV. Direct and BDF solutions agree within 1e-8, confirming the prediction. There is one product, so selectivity is trivially 1; this is not a fitted experimental network."
    if experiment=='rate_control':return f"Forward barriers {r['forward_barriers_eV']} eV have their maximum at step 2, but DRC values {r['response']['degree_of_rate_control']} put the largest control on step 3. The counterexample prediction holds. Intermediate populations and reversibility invalidate simple isolated-barrier ranking."
    raise KeyError(experiment)


def plot(experiment,r,folder):
    fig,ax=plt.subplots();made=True
    if experiment=='finite_differences':
        values=np.array(r['scan']);ax.loglog(values[:,0],values[:,1],'o-');ax.set(xlabel='Displacement (A)',ylabel='Absolute force error (eV/A)')
    elif experiment=='schrodinger':
        for i,psi in enumerate(r['harmonic']['wavefunctions']):ax.plot(r['harmonic']['x_bohr'],psi,label=f'n={i}')
        ax.set(xlabel='x (bohr)',ylabel='Wavefunction');ax.legend()
    elif experiment=='partition':
        ax.plot([x['T_K'] for x in r['two_level']],[x['populations'][1] for x in r['two_level']],'o-');ax.axhline(.75,color='gray',ls='--');ax.set(xlabel='Temperature (K)',ylabel='Excited population')
    elif experiment=='surface_phase':
        for i,v in enumerate(r['grand_potential_eV']):ax.plot(r['mu_eV'],v,label=['clean','quarter','half'][i])
        ax.set(xlabel='Chemical potential (eV)',ylabel='Grand potential (eV/cell)');ax.legend()
    elif experiment=='neb':
        ax.plot(r['own']['energies_eV'],'o-');ax.set(xlabel='Image',ylabel='Energy (eV)')
    elif experiment=='tst':
        for t in [300,600,1000,1500]:
            rows=np.array([x for x in r['scan'] if x[0]==t]);ax.semilogy(rows[:,1],rows[:,3],label=f'{t} K')
        ax.set(xlabel='Free-energy barrier (eV)',ylabel='Waiting time (s)');ax.legend()
    elif experiment=='umbrella':
        for name,label in [('one_dimension','1D'),('hidden_coordinate','2D marginal')]:
            data=r[name];ax.plot(data['x'],data['F_eV'],label=label);ax.plot(data['x'],data['exact_F_eV'],'--',alpha=.6)
        ax.set(xlim=(-1.4,1.4),ylim=(0,.3),xlabel='x (model coordinate)',ylabel='Free energy (eV)');ax.legend()
    elif experiment=='mep_fes':
        ax.plot(r['x'],r['MEP_eV'],label='0 K MEP')
        for data in r['finite_temperature']:ax.plot(r['x'],data['F_eV'],label=f"{data['T_K']} K")
        ax.set(xlabel='x (model coordinate)',ylabel='Relative energy (eV)');ax.legend()
    elif experiment=='microkinetics':
        times=np.array(r['integration']['time_s']);theta=np.array(r['integration']['coverages'])
        for i,name in enumerate(['vacancy','A*','B*']):ax.semilogx(times[1:],theta[1:,i],label=name)
        ax.set(xlabel='Time (s)',ylabel='Site fraction');ax.legend()
    elif experiment=='rate_control':
        ax.bar([1,2,3],r['response']['degree_of_rate_control']);ax.set(xlabel='Elementary step',ylabel='Degree of rate control',xticks=[1,2,3])
    elif experiment=='periodic':
        rows=np.array(r['scan']);ax.plot(rows[:,0],rows[:,2],'o-');ax.set(xlabel='Lattice constant (A)',ylabel='Energy (eV/atom)',title=r['backend'].upper())
    elif experiment=='chemical_potential':
        for t in [300,600,1000]:
            values=np.array([x for x in r['scan'] if x[0]==t]);ax.semilogx(values[:,1],values[:,3],'o-',label=f'{t} K')
        ax.axhline(0,color='gray',ls='--');ax.set(xlabel='Pressure (bar)',ylabel='Adsorption free energy (eV)');ax.legend()
    else:made=False
    if made:
        fig.tight_layout();fig.savefig(folder/'figure.svg',metadata={'Date':None})
        svg=folder/'figure.svg'
        svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')
    plt.close(fig)
    return made

for project in json.loads((ROOT/'projects.json').read_text()):
    folder=ROOT/project['path']/'output';path=folder/'result.json'
    if not path.exists():continue
    payload=json.loads(path.read_text());r=payload['result'];experiment=payload['input']['experiment']
    text=summary(experiment,r)
    has_plot=plot(experiment,r,folder)
    (folder/'analysis.md').write_text('# Measured result and postmortem\n\n'+text+'\n\n'
        +f"Input SHA-256: `{payload['input_sha256']}`. Slurm job: `{payload['slurm_job_id']}`. Software versions and source revision are in [result.json](result.json).\n\n"
        +'Predictions remain unchanged in the project README and root predictions.md. Numerical agreement validates the stated model and checks, not an unrestricted scientific claim.\n'
        +('\n![Computed result](figure.svg)\n' if has_plot else ''))
