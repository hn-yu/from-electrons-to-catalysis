# Break rate-determining-step intuition

Distinguish isolated barriers from control over flux.

## Before computing

The largest isolated forward barrier need not have largest DRC; medium confidence. Falsifier: this input gives the same ranking.

This prediction was recorded before the example run. Results and diagnoses are appended in [output/analysis.md](output/analysis.md); do not rewrite the prediction to match the output.

## Implement it

1. Rank the forward barriers.
2. Perturb shared transition-state energies to obtain degree of rate control.
3. Perturb intermediate and transition-state free energies by ±0.1 eV.

Read [hints](hints/README.md) progressively, then inspect the reference implementation in `src/catalysis/` (experiment `rate_control` in `experiments.py`). Shared algorithms are reused by later projects.

## Run from repository root

```bash
python 06_catalysis/07_rate_control/run.py
# On a Slurm cluster:
sbatch scripts/slurm.sh 06_catalysis/07_rate_control/run.py
```

Dependency tier: **core**. See root installation instructions. Input: [input/example.json](input/example.json). Reference result: [output/result.json](output/result.json). Runs default to `runs/07_rate_control/`, so examples are not overwritten. To reproduce elsewhere, pass `--output PATH`.

## Checks and interpretation

Detailed balance after perturbation; DRC sum near 1; nonlinear ±0.1 eV response.

The root pytest suite supplies numerical, physical and limiting-case checks. Compare floating-point values with tolerances, not byte-for-byte JSON equality; software versions and scheduler IDs are provenance, not numerical targets. The result and analysis identify the model and its limits.

## Interpret the actual counterexample

In the included run the forward barriers are 0.65, 0.90 and 0.55 eV. Yet transition-state degrees of rate control are approximately 0.026, 0.003 and 0.971. Raising the third transition state by 0.1 eV reduces TOF to about 0.148 of its original value; raising the second transition state by the same amount gives about 0.983. The highest isolated forward barrier therefore has very little control here. Deep intermediate stabilization and reverse cycling matter: the probability that an excursion produces a product is part of the flux calculation.
