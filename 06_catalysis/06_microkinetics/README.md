# Microkinetics and observables

Solve site populations and compare a direct steady state with time integration.

## Before computing

Coverages positive and sum to 1; steady TOF positive; integrated and algebraic populations agree to 1e-6. High confidence.

This prediction was recorded before the example run. Results and diagnoses are appended in [output/analysis.md](output/analysis.md); do not rewrite the prediction to match the output.

## Implement it

1. Build the mass-action generator with column sums zero.
2. Replace one redundant equation by site normalization.
3. Integrate with BDF as an independent numerical check.
4. Compute TOF, reaction orders and apparent activation.

Read [hints](hints/README.md) progressively, then inspect the reference implementation in `src/catalysis/` (experiment `microkinetics` in `experiments.py`). Shared algorithms are reused by later projects.

## Run from repository root

```bash
python 06_catalysis/06_microkinetics/run.py
# On a Slurm cluster:
sbatch scripts/slurm.sh 06_catalysis/06_microkinetics/run.py
```

Dependency tier: **core**. See root installation instructions. Input: [input/example.json](input/example.json). Reference result: [output/result.json](output/result.json). Runs default to `runs/06_microkinetics/`, so examples are not overwritten. To reproduce elsewhere, pass `--output PATH`.

## Checks and interpretation

ODE/direct agreement; site conservation; zero TOF at thermodynamic equilibrium.

The root pytest suite supplies numerical, physical and limiting-case checks. Compare floating-point values with tolerances, not byte-for-byte JSON equality; software versions and scheduler IDs are provenance, not numerical targets. The result and analysis identify the model and its limits.
