"""An unchanged restart is reusable; changed physics must trigger recomputation."""
from catalysis import surfaces


def test_restart_invalidates_input_and_paw_data(tmp_path,monkeypatch):
    calls=[]
    dataset={'Cu':'first'}
    def calculate(config,work):
        calls.append(config.copy())
        return {'energy':float(len(calls))}
    monkeypatch.setattr(surfaces,'adsorption',calculate)
    monkeypatch.setattr(surfaces,'paw_fingerprints',lambda config:dataset.copy())
    config={'backend':'emt','size':[2,2,3]}
    assert surfaces.cached_adsorption(config,tmp_path)['energy']==1
    assert surfaces.cached_adsorption(config,tmp_path)['energy']==1
    dataset['Cu']='replaced-at-the-same-path'
    assert surfaces.cached_adsorption(config,tmp_path)['energy']==2
    assert surfaces.cached_adsorption({**config,'size':[2,2,4]},tmp_path)['energy']==3
    assert len(calls)==3
