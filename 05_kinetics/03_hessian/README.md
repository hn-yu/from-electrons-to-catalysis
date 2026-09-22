# Hessians and normal modes

Classify stationary points through curvature.

## Before computing

MB minimum has zero negative modes; saddle has exactly one. High confidence.

This prediction was recorded before the example run. Results and diagnoses are appended in [output/analysis.md](output/analysis.md); do not rewrite the prediction to match the output.

## Implement it

1. Difference forces with the required minus sign.
2. Symmetrize and mass-weight.
3. Inspect the unstable MB saddle eigenvector.

Read [hints](hints/README.md) progressively, then inspect the reference implementation in `src/catalysis/` (experiment `hessian` in `experiments.py`). Shared algorithms are reused by later projects.

## Run from repository root

```bash
python 05_kinetics/03_hessian/run.py
# On a Slurm cluster:
sbatch scripts/slurm.sh 05_kinetics/03_hessian/run.py
```

Dependency tier: **core**. See root installation instructions. Input: [input/example.json](input/example.json). Reference result: [output/result.json](output/result.json). Runs default to `runs/03_hessian/`, so examples are not overwritten. To reproduce elsewhere, pass `--output PATH`.

## Checks and interpretation

Hessian symmetry; minimum/saddle inertia; Morse analytic curvature.

The root pytest suite supplies numerical, physical and limiting-case checks. Compare floating-point values with tolerances, not byte-for-byte JSON equality; software versions and scheduler IDs are provenance, not numerical targets. The result and analysis identify the model and its limits.
