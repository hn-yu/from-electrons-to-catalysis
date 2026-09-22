# Executed PBE adsorption-site comparison

Cu(111), 2×2×3 slab, 0.25 ML H, PBE, 300 eV plane waves, 3×3×1 k mesh and one fixed bottom layer. All references are recomputed with compatible settings.

| Initial site | Adsorption energy (eV/H) | Maximum movable force (eV/A) |
|---|---:|---:|
| ontop | +0.531111 | 0.033191 |
| bridge | +0.048063 | 0.039474 |
| fcc | -0.089783 | 0.027254 |
| hcp | -0.082735 | 0.032487 |

The predicted hollow-site preference can be assessed from the actual values, but initial labels must be checked against final coordinates in the accompanying extxyz files. Symmetry-preserving optimization can retain a lateral saddle, so a site is not proven metastable from a small gradient alone.

The separate real-system thickness audit found a large 3→4-layer effect. Therefore these site results are executed bringup examples, not numerically converged adsorption predictions. Compare sites again on a thickness-converged common slab before using a small energy difference as chemical evidence. The original prediction is retained rather than rewritten from this ranking.

This long run launched at commit `3debe47` before the relaxation point-group fix. Its launch provenance is explicitly retained in result.json; current code disables point-group symmetry. Floating-point equality across those implementations is not asserted.

Adsorption energies use the default extrapolated electronic energies for every reference. Optimizer log energies may be force-consistent finite-occupation free energies and need not equal the JSON total energies. Electronic smearing is not the thermodynamic gas temperature.

Prediction-log limitation: the site's original qualitative ordering prediction explicitly concerned EMT. This PBE calculation tests transfer of that coordination intuition; it is not presented as an independently preregistered quantitative PBE site-ranking prediction. Preserve that distinction when assessing calibration.
