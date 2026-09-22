# Adsorption site competition

Compare symmetry-distinct initial adsorption sites.

## Before computing

Hollow sites likely below atop for this toy EMT setup; low confidence. Falsifier: optimized ordering reverses.

This prediction was recorded before the example run. Results and diagnoses are appended in [output/analysis.md](output/analysis.md); do not rewrite the prediction to match the output.

## Implement it

1. Predict site order.
2. Relax each structure under the same model.
3. Report final coordinates to detect site migration.

Read [hints](hints/README.md) progressively, then inspect the reference implementation in `src/catalysis/` (experiment `adsorption` in `experiments.py`). Shared algorithms are reused by later projects.

## Run from repository root

```bash
python 06_catalysis/02_adsorption/run.py
# On a Slurm cluster:
sbatch scripts/slurm.sh 06_catalysis/02_adsorption/run.py
```

Dependency tier: **core**. See root installation instructions. Input: [input/example.json](input/example.json). Reference result: [output/result.json](output/result.json). Runs default to `runs/02_adsorption/`, so examples are not overwritten. To reproduce elsewhere, pass `--output PATH`.

## Checks and interpretation

Energy reference; force convergence; final-site inspection.

The root pytest suite supplies numerical, physical and limiting-case checks. Compare floating-point values with tolerances, not byte-for-byte JSON equality; software versions and scheduler IDs are provenance, not numerical targets. The result and analysis identify the model and its limits.
