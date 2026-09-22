# Break finite differences

Expose cancellation and truncation error.

## Before computing

The best h lies between 1e-7 and 1e-4 A; errors rise at both extremes. Medium confidence; falsified by monotonic error.

This prediction was recorded before the example run. Results and diagnoses are appended in [output/analysis.md](output/analysis.md); do not rewrite the prediction to match the output.

## Implement it

1. Sweep displacements over fourteen decades.
2. Locate the error minimum.
3. Explain why a small difference between two bad derivatives proves little.

Read [hints](hints/README.md) progressively, then inspect the reference implementation in `src/catalysis/` (experiment `finite_differences` in `experiments.py`). Shared algorithms are reused by later projects.

## Run from repository root

```bash
python 02_bringup/03_finite_differences/run.py
# On a Slurm cluster:
sbatch scripts/slurm.sh 02_bringup/03_finite_differences/run.py
```

Dependency tier: **core**. See root installation instructions. Input: [input/example.json](input/example.json). Reference result: [output/result.json](output/result.json). Runs default to `runs/03_finite_differences/`, so examples are not overwritten. To reproduce elsewhere, pass `--output PATH`.

## Checks and interpretation

Interior error minimum; correct force sign; large-step versus tiny-step error.

The root pytest suite supplies numerical, physical and limiting-case checks. Compare floating-point values with tolerances, not byte-for-byte JSON equality; software versions and scheduler IDs are provenance, not numerical targets. The result and analysis identify the model and its limits.
