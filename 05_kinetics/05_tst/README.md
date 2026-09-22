# Barrier-to-timescale map

Turn a free-energy barrier into a conditional rate estimate.

## Before computing

A 1 eV barrier is very slow at 300 K and much faster at 1000 K; high confidence.

This prediction was recorded before the example run. Results and diagnoses are appended in [output/analysis.md](output/analysis.md); do not rewrite the prediction to match the output.

## Implement it

1. Implement Eyring and Arrhenius forms.
2. Generate a 0–3 eV map and its inverse rates.
3. Explain standard state and transmission assumptions.

Read [hints](hints/README.md) progressively, then inspect the reference implementation in `src/catalysis/` (experiment `tst` in `experiments.py`). Shared algorithms are reused by later projects.

## Run from repository root

```bash
python 05_kinetics/05_tst/run.py
# On a Slurm cluster:
sbatch scripts/slurm.sh 05_kinetics/05_tst/run.py
```

Dependency tier: **core**. See root installation instructions. Input: [input/example.json](input/example.json). Reference result: [output/result.json](output/result.json). Runs default to `runs/05_tst/`, so examples are not overwritten. To reproduce elsewhere, pass `--output PATH`.

## Checks and interpretation

Zero-barrier prefactor; monotonic barrier dependence; inverse rate timescale.

The root pytest suite supplies numerical, physical and limiting-case checks. Compare floating-point values with tolerances, not byte-for-byte JSON equality; software versions and scheduler IDs are provenance, not numerical targets. The result and analysis identify the model and its limits.
