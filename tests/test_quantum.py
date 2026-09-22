import numpy as np
import pytest
pytest.importorskip('pyscf')
from catalysis.electronic import rhf

@pytest.mark.quantum
@pytest.mark.parametrize('atom,charge,electrons',[('H 0 0 0; H 0 0 .74',0,2),('He 0 0 0; H 0 0 .77',1,2),('Li 0 0 0; H 0 0 1.6',0,4)])
def test_scf_reference_electron_count_stationarity(atom,charge,electrons):
    result=rhf(atom,charge=charge)
    assert abs(result['error_Hartree'])<1e-8
    assert result['electrons']==pytest.approx(electrons,abs=1e-10)
    assert result['history'][-1][3]<4e-5

@pytest.mark.quantum
def test_scf_failure_is_explicit():
    with pytest.raises(RuntimeError):rhf('Li 0 0 0; H 0 0 1.6',maxiter=1)
