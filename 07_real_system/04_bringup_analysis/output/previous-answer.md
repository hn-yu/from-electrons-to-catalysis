# Worked bringup: H/Cu(111) adsorption

The 1 ML, 1×1×3 PBE baseline adsorption energy is **+0.045601 eV per H**, relative to half a relaxed H2 molecule. The unchanged pre-run range was -0.8 to +0.3 eV with low confidence. Being inside that broad interval does not resolve the adsorption sign when numerical sensitivity is larger than the baseline energy.

| Axis | Setting | Adsorption energy (eV) | Change from baseline (eV) |
|---|---|---:|---:|
| cutoff_eV | `300` | +0.053326 | +0.007724 |
| kpts | `[4, 4, 1]` | +0.017544 | -0.028058 |
| vacuum_A | `8.0` | +0.050763 | +0.005161 |
| size | `[1, 1, 4]` | -0.301817 | -0.347418 |
| size | `[2, 2, 3]` | -0.088512 | -0.134114 |
| fixed_layers | `0` | +0.048627 | +0.003025 |
| smearing_eV | `0.05` | +0.053070 | +0.007468 |

The pre-run numerical target was 0.05 eV. All sampled changes below target: **False**. The four-layer result exposes a large thickness error in the initial slab. The 2×2×3 result additionally changes coverage to 0.25 ML, so it cannot be interpreted as a pure numerical cell-size check.

The implementation completed its calculations, but the original thin-slab numerical-convergence hypothesis failed. Every task's input, matching clean-slab/H2 energies and final adsorbate coordinates are archived as `task_result.json` alongside the final `fcc.extxyz`. The aggregate stores a truthful failure flag instead of relabeling these numbers as converged DFT adsorption chemistry.

Next cheapest falsification: hold one monolayer, k density, cutoff and reference protocol fixed and extend the layer sequence beyond four. Check thickness oscillations before spending on more sites or NEB. Once a stable slab protocol exists, compare multiple sites at common settings and add vibrational and reservoir corrections before finite-temperature interpretation.

A force-converged geometry is still not automatically a verified minimum; inspect lateral curvature and competing structures. A finite-slab PBE energy does not by itself predict turnover, selectivity or an experimental mechanism.
