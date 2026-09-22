# An energy/force interface

Implement and validate the sign and units of an analytic force.

## Before computing

Force vanishes at 0.74 A; compressed bonds repel and stretched bonds attract. Error <1e-6 eV/A; high confidence.

This prediction was recorded before the example run. Results and diagnoses are appended in [output/analysis.md](output/analysis.md); do not rewrite the prediction to match the output.

## Implement it

1. Differentiate the Morse energy.
2. Scan compressed and stretched bonds.
3. Verify force zero and positive curvature at equilibrium.

Read [hints](hints/README.md) progressively, then inspect the reference implementation in `src/catalysis/` (experiment `forces` in `experiments.py`). Shared algorithms are reused by later projects.

## Run from repository root

```bash
python 02_bringup/02_forces/run.py
# On a Slurm cluster:
sbatch scripts/slurm.sh 02_bringup/02_forces/run.py
```

Dependency tier: **core**. See root installation instructions. Input: [input/example.json](input/example.json). Reference result: [output/result.json](output/result.json). Runs default to `runs/02_forces/`, so examples are not overwritten. To reproduce elsewhere, pass `--output PATH`.

## Checks and interpretation

Analytic/finite difference agreement; force sign; dissociation limit.

The root pytest suite supplies numerical, physical and limiting-case checks. Compare floating-point values with tolerances, not byte-for-byte JSON equality; software versions and scheduler IDs are provenance, not numerical targets. The result and analysis identify the model and its limits.
