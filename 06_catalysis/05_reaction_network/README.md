# Detailed-balance reaction network

Represent a three-step reversible catalytic cycle.

## Before computing

Log detailed-balance residual near machine precision; high confidence.

This prediction was recorded before the example run. Results and diagnoses are appended in [output/analysis.md](output/analysis.md); do not rewrite the prediction to match the output.

## Implement it

1. Define free energies, transition states and stoichiometry.
2. Derive forward and reverse barriers from shared states.
3. Check local detailed balance and site conservation.

Read [hints](hints/README.md) progressively, then inspect the reference implementation in `src/catalysis/` (experiment `reaction_network` in `experiments.py`). Shared algorithms are reused by later projects.

## Run from repository root

```bash
python 06_catalysis/05_reaction_network/run.py
# On a Slurm cluster:
sbatch scripts/slurm.sh 06_catalysis/05_reaction_network/run.py
```

Dependency tier: **core**. See root installation instructions. Input: [input/example.json](input/example.json). Reference result: [output/result.json](output/result.json). Runs default to `runs/05_reaction_network/`, so examples are not overwritten. To reproduce elsewhere, pass `--output PATH`.

## Checks and interpretation

Detailed balance; column site balance; equilibrium cycle product.

The root pytest suite supplies numerical, physical and limiting-case checks. Compare floating-point values with tolerances, not byte-for-byte JSON equality; software versions and scheduler IDs are provenance, not numerical targets. The result and analysis identify the model and its limits.
