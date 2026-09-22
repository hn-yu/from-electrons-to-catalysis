# A 1D Schrodinger solver

Construct a finite-difference Hamiltonian in atomic units.

## Before computing

Harmonic energies start at 0.5 Eh; states have 0,1,2,3 nodes; double well has a small positive splitting. High confidence.

This prediction was recorded before the example run. Results and diagnoses are appended in [output/analysis.md](output/analysis.md); do not rewrite the prediction to match the output.

## Implement it

1. Impose Dirichlet walls using interior grid points.
2. Solve box, oscillator, finite well and double well.
3. Count nodes and repeat with a finer grid and larger box.

Read [hints](hints/README.md) progressively, then inspect the reference implementation in `src/catalysis/` (experiment `schrodinger` in `experiments.py`). Shared algorithms are reused by later projects.

## Run from repository root

```bash
python 03_electronic_structure/01_schrodinger/run.py
# On a Slurm cluster:
sbatch scripts/slurm.sh 03_electronic_structure/01_schrodinger/run.py
```

Dependency tier: **core**. See root installation instructions. Input: [input/example.json](input/example.json). Reference result: [output/result.json](output/result.json). Runs default to `runs/01_schrodinger/`, so examples are not overwritten. To reproduce elsewhere, pass `--output PATH`.

## Checks and interpretation

Box analytic spectrum; oscillator zero-point energy; grid normalization and ordering.

The root pytest suite supplies numerical, physical and limiting-case checks. Compare floating-point values with tolerances, not byte-for-byte JSON equality; software versions and scheduler IDs are provenance, not numerical targets. The result and analysis identify the model and its limits.
