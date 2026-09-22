"""Exercise native scientific input and independent reference paths."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import numpy as np
import pytest
ROOT=Path(__file__).resolve().parents[1]


def run(path,folder,output):
    subprocess.run([sys.executable,str(ROOT/path/'run.py'),'--input',str(folder),'--output',str(output)],check=True,capture_output=True,text=True)
    return json.loads((output/'result.json').read_text())


def test_xyz_changes_force_and_audit(tmp_path):
    from ase.io import read,write
    path=Path('02_bringup/02_forces');folder=tmp_path/'input';shutil.copytree(ROOT/path/'input',folder)
    first=run(path,folder,tmp_path/'first')
    atoms=read(folder/'bonds.xyz');atoms.positions[1]=atoms.positions[0]+[1.1,.2,0]
    write(folder/'bonds.xyz',atoms)
    changed=run(path,folder,tmp_path/'changed')
    row=changed['result']['scan'][0]
    assert row[0]==pytest.approx(np.sqrt(1.1**2+.2**2))
    assert row[1]!=pytest.approx(first['result']['scan'][0][1])
    assert row[3]==pytest.approx(row[4],abs=1e-12)
    assert first['input_files_sha256']['bonds.xyz']!=changed['input_files_sha256']['bonds.xyz']


@pytest.mark.quantum
@pytest.mark.parametrize('name',['H2','HeHplus','LiH','H2O'])
def test_cached_ao_integrals_match_xyz(name):
    pytest.importorskip('pyscf')
    from pyscf import gto
    from catalysis.integral_files import load_integrals
    from catalysis.teaching_io import read_xyz,atom_string
    folder=ROOT/'03_electronic_structure/03_rhf/input'/name
    mol=gto.M(atom=atom_string(read_xyz(folder/'molecule.xyz')),basis='sto-3g',charge=int(name=='HeHplus'),verbose=0)
    s,h,eri,n,enuc=load_integrals(folder)
    np.testing.assert_allclose(s,mol.intor('int1e_ovlp'),atol=1e-12)
    np.testing.assert_allclose(h,mol.intor('int1e_kin')+mol.intor('int1e_nuc'),atol=1e-12)
    np.testing.assert_allclose(eri,mol.intor('int2e'),atol=1e-12)
    assert n==mol.nelectron and enuc==pytest.approx(mol.energy_nuc(),abs=1e-12)


@pytest.mark.parametrize('temperature,pa,pb',[(400,.1,.01),(600,1,.01),(900,10,.1)])
def test_cantera_independent_coverage_and_flux(temperature,pa,pb):
    pytest.importorskip('cantera')
    from catalysis.cantera_reference import solve,model_from_tables
    from catalysis.network import steady_state
    folder=ROOT/'06_catalysis/06_microkinetics/input'
    own=steady_state(model_from_tables(folder),temperature,pa,pb)
    ref=solve(folder/'mechanism.yaml',temperature,pa,pb)
    np.testing.assert_allclose(own['coverages'],ref['coverages'],rtol=1e-7,atol=1e-10)
    np.testing.assert_allclose(own['elementary_rates_s^-1'],ref['elementary_rates_s^-1'],rtol=1e-7)


def test_published_independent_algorithms():
    def result(path):return json.loads((ROOT/path/'output/result.json').read_text())['result']
    assert result('05_kinetics/02_dynamics')['max_position_difference_A']<1e-10
    for name in ['one_dimension','hidden_coordinate']:
        assert result('06_catalysis/03_umbrella')[name]['PyMBAR_shape_RMSE_eV']<.002
    r=result('06_catalysis/07_rate_control')
    np.testing.assert_allclose(r['response']['degree_of_rate_control'],r['Cantera_degree_of_rate_control'],atol=1e-5)
