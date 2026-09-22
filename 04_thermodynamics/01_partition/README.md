# Partition functions

Derive entropy from state counting.

## Before computing

Excited population rises toward 3/4; oscillator U tends to 0.06 eV at low T. High confidence.

This prediction was recorded before the example run. Results and diagnoses are appended in [output/analysis.md](output/analysis.md); do not rewrite the prediction to match the output.

## Implement it

1. Use log-sum-exp for Z.
2. Compute populations, U, F and S including degeneracy.
3. Sum the harmonic-oscillator ladder analytically.

Read [hints](hints/README.md) progressively, then inspect the reference implementation in `src/catalysis/` (experiment `partition` in `experiments.py`). Shared algorithms are reused by later projects.

## Run from repository root

```bash
python 04_thermodynamics/01_partition/run.py
# On a Slurm cluster:
sbatch scripts/slurm.sh 04_thermodynamics/01_partition/run.py
```

Dependency tier: **core**. See root installation instructions. Input: [input/example.json](input/example.json). Reference result: [output/result.json](output/result.json). Runs default to `runs/01_partition/`, so examples are not overwritten. To reproduce elsewhere, pass `--output PATH`.

## Checks and interpretation

Population normalization; U-F=TS; high/low-temperature limits.

The root pytest suite supplies numerical, physical and limiting-case checks. Compare floating-point values with tolerances, not byte-for-byte JSON equality; software versions and scheduler IDs are provenance, not numerical targets. The result and analysis identify the model and its limits.
