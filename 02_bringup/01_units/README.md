# Units and physical scales

Convert numbers into physical scales.

## Before computing

kBT is about 0.026, 0.052, 0.086, 0.129 eV; high confidence from linear scaling. Falsifier: >2% discrepancy.

This prediction was recorded before the example run. Results and diagnoses are appended in [output/analysis.md](output/analysis.md); do not rewrite the prediction to match the output.

## Implement it

1. Implement dimension-checked conversions.
2. Compute kBT without treating Kelvin as an energy.
3. Compare thermal energy with bond energies.

Read [hints](hints/README.md) progressively, then inspect the reference implementation in `src/catalysis/` (experiment `units_experiment` in `experiments.py`). Shared algorithms are reused by later projects.

## Run from repository root

```bash
python 02_bringup/01_units/run.py
# On a Slurm cluster:
sbatch scripts/slurm.sh 02_bringup/01_units/run.py
```

Dependency tier: **core**. See root installation instructions. Input: [input/example.json](input/example.json). Reference result: [output/result.json](output/result.json). Runs default to `runs/01_units/`, so examples are not overwritten. To reproduce elsewhere, pass `--output PATH`.

## Checks and interpretation

Round trips; linear temperature scaling; incompatible dimensions rejected.

The root pytest suite supplies numerical, physical and limiting-case checks. Compare floating-point values with tolerances, not byte-for-byte JSON equality; software versions and scheduler IDs are provenance, not numerical targets. The result and analysis identify the model and its limits.
