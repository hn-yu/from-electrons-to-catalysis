# Real DFT bringup

Carry one H/Cu(111) adsorption subproblem through an explicit DFT convergence audit.

## Before computing

PBE H/Cu(111) adsorption relative to half H2 expected -0.8 to +0.3 eV; low confidence. Falsifier: outside range or unstable final adsorption geometry.

This prediction was recorded before the example run. Results and diagnoses are appended in [output/analysis.md](output/analysis.md); do not rewrite the prediction to match the output.

## Implement it

1. Read the committed calculation memo and prediction first.
2. Run the shared slab workflow using PBE/GPAW with no EMT fallback.
3. Inspect each convergence axis and final site.
4. Separate six assertions: SCF, geometry, numerical, state, model and claim.

Read [hints](hints/README.md) progressively, then inspect the reference implementation in `src/catalysis/` (experiment `slab` in `experiments.py`). Shared algorithms are reused by later projects.

## Run from repository root

```bash
python 07_real_system/02_real_dft/run.py
# On a Slurm cluster:
sbatch scripts/slurm.sh 07_real_system/02_real_dft/run.py
```

Dependency tier: **periodic**. See root installation instructions. Input: [input/example.json](input/example.json). Reference result: [output/result.json](output/result.json). Runs default to `runs/02_real_dft/`, so examples are not overwritten. To reproduce elsewhere, pass `--output PATH`.

## Checks and interpretation

Relaxed forces; matching H2 and slab references; all numerical axes versus 0.05 eV.

The root pytest suite supplies numerical, physical and limiting-case checks. Compare floating-point values with tolerances, not byte-for-byte JSON equality; software versions and scheduler IDs are provenance, not numerical targets. The result and analysis identify the model and its limits.
