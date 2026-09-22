# Optimization

Find local minima using steepest descent and backtracking.

## Before computing

Morse converges to 0.74 A; MB starts find at least two minima. High confidence.

This prediction was recorded before the example run. Results and diagnoses are appended in [output/analysis.md](output/analysis.md); do not rewrite the prediction to match the output.

## Implement it

1. Implement an Armijo line search.
2. Reuse analytic forces.
3. Compare multiple starting basins.

Read [hints](hints/README.md) progressively, then inspect the reference implementation in `src/catalysis/` (experiment `optimizer` in `experiments.py`). Shared algorithms are reused by later projects.

## Run from repository root

```bash
python 05_kinetics/01_optimizer/run.py
# On a Slurm cluster:
sbatch scripts/slurm.sh 05_kinetics/01_optimizer/run.py
```

Dependency tier: **core**. See root installation instructions. Input: [input/example.json](input/example.json). Reference result: [output/result.json](output/result.json). Runs default to `runs/01_optimizer/`, so examples are not overwritten. To reproduce elsewhere, pass `--output PATH`.

## Checks and interpretation

Small residual forces; Morse exact minimum; multiple basins.

The root pytest suite supplies numerical, physical and limiting-case checks. Compare floating-point values with tolerances, not byte-for-byte JSON equality; software versions and scheduler IDs are provenance, not numerical targets. The result and analysis identify the model and its limits.
