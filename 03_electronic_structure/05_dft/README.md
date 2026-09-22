# HF, density functionals and FCI

Compare approximations at identical geometry and basis.

## Before computing

FCI <= RHF; the difference grows on stretching. Functionals disagree despite SCF convergence; high confidence.

This prediction was recorded before the example run. Results and diagnoses are appended in [output/analysis.md](output/analysis.md); do not rewrite the prediction to match the output.

## Implement it

1. Run restricted HF, LDA, PBE and B3LYP.
2. Compute a same-basis FCI reference.
3. Separate finite-basis exactness from complete-basis accuracy.

Read [hints](hints/README.md) progressively, then inspect the reference implementation in `src/catalysis/` (experiment `dft` in `experiments.py`). Shared algorithms are reused by later projects.

## Run from repository root

```bash
python 03_electronic_structure/05_dft/run.py
# On a Slurm cluster:
sbatch scripts/slurm.sh 03_electronic_structure/05_dft/run.py
```

Dependency tier: **quantum**. See root installation instructions. Input: [input/example.json](input/example.json). Reference result: [output/result.json](output/result.json). Runs default to `runs/05_dft/`, so examples are not overwritten. To reproduce elsewhere, pass `--output PATH`.

## Checks and interpretation

FCI variational ordering; repeatable functional energies; stretched versus equilibrium correlation error.

The root pytest suite supplies numerical, physical and limiting-case checks. Compare floating-point values with tolerances, not byte-for-byte JSON equality; software versions and scheduler IDs are provenance, not numerical targets. The result and analysis identify the model and its limits.
