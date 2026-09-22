# Nonorthogonal LCAO

Solve Hc=ESc without pretending an AO basis is orthogonal.

## Before computing

Energies are approximately -1.0833 and -0.875 Eh; lower eigenvector is bonding. High confidence.

This prediction was recorded before the example run. Results and diagnoses are appended in [output/analysis.md](output/analysis.md); do not rewrite the prediction to match the output.

## Implement it

1. Check positive definiteness of overlap.
2. Diagonalize in the orthogonalized basis.
3. Compare full-space energy with a one-vector Rayleigh quotient.

Read [hints](hints/README.md) progressively, then inspect the reference implementation in `src/catalysis/` (experiment `lcao` in `experiments.py`). Shared algorithms are reused by later projects.

## Run from repository root

```bash
python 03_electronic_structure/02_lcao/run.py
# On a Slurm cluster:
sbatch scripts/slurm.sh 03_electronic_structure/02_lcao/run.py
```

Dependency tier: **core**. See root installation instructions. Input: [input/example.json](input/example.json). Reference result: [output/result.json](output/result.json). Runs default to `runs/02_lcao/`, so examples are not overwritten. To reproduce elsewhere, pass `--output PATH`.

## Checks and interpretation

Generalized residual; S orthogonality; zero-overlap limit and variational upper bound.

The root pytest suite supplies numerical, physical and limiting-case checks. Compare floating-point values with tolerances, not byte-for-byte JSON equality; software versions and scheduler IDs are provenance, not numerical targets. The result and analysis identify the model and its limits.
