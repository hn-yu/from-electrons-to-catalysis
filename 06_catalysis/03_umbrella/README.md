# Umbrella sampling and WHAM

Reconstruct an unbiased free-energy profile and reveal bad coordinates.

## Before computing

WHAM shape error <0.03 eV; adjacent windows overlap; hidden high-barrier y retains its initial sign. Medium confidence.

This prediction was recorded before the example run. Results and diagnoses are appended in [output/analysis.md](output/analysis.md); do not rewrite the prediction to match the output.

## Implement it

1. Metropolis sample overlapping biased windows.
2. Iterate log-domain WHAM with one offset gauge fixed.
3. Compare exact 1D and analytically marginalized 2D profiles.
4. Run two starts in a hidden metastable coordinate.

Read [hints](hints/README.md) progressively, then inspect the reference implementation in `src/catalysis/` (experiment `umbrella` in `experiments.py`). Shared algorithms are reused by later projects.

## Run from repository root

```bash
python 06_catalysis/03_umbrella/run.py
# On a Slurm cluster:
sbatch scripts/slurm.sh 06_catalysis/03_umbrella/run.py
```

Dependency tier: **core**. See root installation instructions. Input: [input/example.json](input/example.json). Reference result: [output/result.json](output/result.json). Runs default to `runs/03_umbrella/`, so examples are not overwritten. To reproduce elsewhere, pass `--output PATH`.

## Checks and interpretation

WHAM self-consistency; exact marginal comparison; overlap and independent-start diagnostic.

The root pytest suite supplies numerical, physical and limiting-case checks. Compare floating-point values with tolerances, not byte-for-byte JSON equality; software versions and scheduler IDs are provenance, not numerical targets. The result and analysis identify the model and its limits.
