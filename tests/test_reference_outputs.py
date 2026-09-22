"""Optional completed-example checks, including long-run numerical/physical assertions."""
import json
from pathlib import Path
import numpy as np
import pytest
ROOT=Path(__file__).resolve().parents[1]

def result(project):
    path=ROOT/project/'output/result.json'
    if not path.exists():pytest.skip('Generate reference examples first')
    return json.loads(path.read_text())['result']

def test_ase_neb_reference():
    r=result('05_kinetics/04_neb')
    assert abs(r['barrier_difference_eV'])<.03
    assert r['own']['force_max']<2e-4
    assert .8<r['own']['barrier_eV']<1.2

def test_umbrella_marginal_and_mixing():
    r=result('06_catalysis/03_umbrella')
    for name in ['one_dimension','hidden_coordinate']:
        assert r[name]['shape_RMSE_eV']<.03
        assert min(r[name]['adjacent_overlap_bins'])>0
        assert all(0<a<1 for a in r[name]['acceptance'])
    assert r['bad_coordinate'][0]['mean_y']<0<r['bad_coordinate'][1]['mean_y']

def test_molecular_rrho_reference_and_modes():
    r=result('04_thermodynamics/02_molecular_thermochemistry')
    for row,modes in zip(r['results'],[1,1,4,3]):
        assert abs(row['G_error_eV'])<1e-4
        assert len(row['frequencies_cm^-1'])==modes
        assert min(row['frequencies_cm^-1'])>0
        assert row['S_eV_K']>0

def test_hf_breaking_and_fci_variation():
    hf=result('03_electronic_structure/04_break_hf')
    assert hf['stretch'][-1]['UHF_Hartree']<hf['stretch'][-1]['RHF_Hartree']-.1
    assert hf['stretch'][-1]['UHF_S2']==pytest.approx(1,abs=.01)
    dft=result('03_electronic_structure/05_dft')
    assert all(r['FCI_Hartree']<=r['HF_Hartree']+1e-10 for r in dft['results'])

def test_rate_control_counterexample():
    r=result('06_catalysis/07_rate_control')
    assert np.argmax(r['forward_barriers_eV'])!=np.argmax(r['response']['degree_of_rate_control'])
    assert sum(r['response']['degree_of_rate_control'])==pytest.approx(1,abs=1e-4)

def test_eos_and_slab_bookkeeping():
    r=result('03_electronic_structure/06_periodic')
    assert 3.8<r['a0_A']<4.2 and r['bulk_modulus_GPa']>0
    r=result('06_catalysis/02_adsorption')
    for site in r['sites']:
        assert site['adsorption_eV']==pytest.approx(site['total_eV']-r['clean_eV']-.5*r['H2_eV'])
        assert site['force_max_eV_A']<=.041

def test_atomic_diffusion_reference():
    path=ROOT/'05_kinetics/04_neb/output/atom_diffusion/result.json'
    if not path.exists():pytest.skip('Atomic continuation not generated')
    r=json.loads(path.read_text())['result']
    assert 0<r['barrier_eV']<1
    assert max(r['endpoint_force_max'])<.001
    assert np.linalg.norm(np.array(r['H_positions_A'][0])-r['H_positions_A'][-1])>.1

def test_periodic_dft_reference():
    path=ROOT/'03_electronic_structure/06_periodic/output/dft/result.json'
    if not path.exists():pytest.skip('Periodic reference not generated')
    r=json.loads(path.read_text())['result']
    assert r['backend']=='gpaw'
    assert 3.9<r['a0_A']<4.2
    assert r['bulk_modulus_GPa']>0
    cutoff=[x for x in r['convergence_sweep'] if x['parameter']=='cutoff_eV'][0]
    assert abs(cutoff['a0_A']-r['a0_A'])<.005

def test_real_dft_reference_and_honest_tolerance():
    r=result('07_real_system/02_real_dft')
    assert r['backend']=='gpaw'
    b=r['baseline'];s=b['sites'][0]
    assert s['adsorption_eV']==pytest.approx(s['total_eV']-b['clean_eV']-.5*b['H2_eV'])
    assert s['force_max_eV_A']<.051
    expected=all(abs(x['delta_from_baseline_eV'])<r['tolerance_eV'] for x in r['sweep'])
    assert r['all_variations_within_tolerance']==expected

def test_pbe_adsorption_sites_reference():
    path=ROOT/'06_catalysis/02_adsorption/output/dft/result.json'
    if not path.exists():pytest.skip('Optional four-site PBE comparison not generated')
    r=json.loads(path.read_text())['result']
    assert r['backend']=='gpaw'
    assert {s['initial_site'] for s in r['sites']}=={'ontop','bridge','fcc','hcp'}
    assert r['coverage_ML']==.25
    for s in r['sites']:
        assert s['adsorption_eV']==pytest.approx(s['total_eV']-r['clean_eV']-.5*r['H2_eV'])
        assert s['force_max_eV_A']<.041
        assert np.all(np.isfinite(s['final_H_position_A']))
