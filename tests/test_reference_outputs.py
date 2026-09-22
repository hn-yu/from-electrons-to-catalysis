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
