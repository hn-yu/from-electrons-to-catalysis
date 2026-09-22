# Pressure and chemical potential

Show why favorable adsorption energy need not imply favorable free energy.

## Before computing

Adsorption deltaE=-0.6 eV but deltaG>0 at 1000 K and 1 bar; high confidence.

This prediction was recorded before the example run. Results and diagnoses are appended in [output/analysis.md](output/analysis.md); do not rewrite the prediction to match the output.

## Implement it

1. Set a 1 bar standard state.
2. Compute mu and adsorption deltaG over T,p.
3. Locate the sign reversal.

Read [hints](hints/README.md) progressively, then inspect the reference implementation in `src/catalysis/` (experiment `chemical_potential` in `experiments.py`). Shared algorithms are reused by later projects.

## Run from repository root

```bash
python 04_thermodynamics/03_chemical_potential/run.py
# On a Slurm cluster:
sbatch scripts/slurm.sh 04_thermodynamics/03_chemical_potential/run.py
```

Dependency tier: **core**. See root installation instructions. Input: [input/example.json](input/example.json). Reference result: [output/result.json](output/result.json). Runs default to `runs/03_chemical_potential/`, so examples are not overwritten. To reproduce elsewhere, pass `--output PATH`.

## Checks and interpretation

p=p0 identity; logarithmic pressure slope; unfavorable low-pressure limit.

The root pytest suite supplies numerical, physical and limiting-case checks. Compare floating-point values with tolerances, not byte-for-byte JSON equality; software versions and scheduler IDs are provenance, not numerical targets. The result and analysis identify the model and its limits.
