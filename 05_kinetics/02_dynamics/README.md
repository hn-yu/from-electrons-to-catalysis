# Velocity Verlet

Separate timestep error from sampling and physical timescales.

## Before computing

Error scales approximately as dt^2 in stable regime; dt>2 fails. High confidence.

This prediction was recorded before the example run. Results and diagnoses are appended in [output/analysis.md](output/analysis.md); do not rewrite the prediction to match the output.

## Implement it

1. Implement position and velocity updates in reduced units.
2. Measure bounded harmonic energy error.
3. Test a finite Lennard-Jones dimer and cross the harmonic stability threshold.

Read [hints](hints/README.md) progressively, then inspect the reference implementation in `src/catalysis/` (experiment `dynamics` in `experiments.py`). Shared algorithms are reused by later projects.

## Run from repository root

```bash
python 05_kinetics/02_dynamics/run.py
# On a Slurm cluster:
sbatch scripts/slurm.sh 05_kinetics/02_dynamics/run.py
```

Dependency tier: **core**. See root installation instructions. Input: [input/example.json](input/example.json). Reference result: [output/result.json](output/result.json). Runs default to `runs/02_dynamics/`, so examples are not overwritten. To reproduce elsewhere, pass `--output PATH`.

## Checks and interpretation

Energy error scaling; momentum conservation; harmonic stability boundary.

The root pytest suite supplies numerical, physical and limiting-case checks. Compare floating-point values with tolerances, not byte-for-byte JSON equality; software versions and scheduler IDs are provenance, not numerical targets. The result and analysis identify the model and its limits.
