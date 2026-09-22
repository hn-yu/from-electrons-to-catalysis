# Surface phase diagram

Take the lower envelope of surface grand potentials.

## Before computing

Clean→quarter→half transitions at mu=-0.5 and -0.2 eV; high confidence.

This prediction was recorded before the example run. Results and diagnoses are appended in [output/analysis.md](output/analysis.md); do not rewrite the prediction to match the output.

## Implement it

1. Use equal-area cells and an explicit adsorbate reference.
2. Compute E-Nmu.
3. Find stability boundaries and list omitted entropy terms.

Read [hints](hints/README.md) progressively, then inspect the reference implementation in `src/catalysis/` (experiment `surface_phase` in `experiments.py`). Shared algorithms are reused by later projects.

## Run from repository root

```bash
python 04_thermodynamics/04_surface_phase/run.py
# On a Slurm cluster:
sbatch scripts/slurm.sh 04_thermodynamics/04_surface_phase/run.py
```

Dependency tier: **core**. See root installation instructions. Input: [input/example.json](input/example.json). Reference result: [output/result.json](output/result.json). Runs default to `runs/04_surface_phase/`, so examples are not overwritten. To reproduce elsewhere, pass `--output PATH`.

## Checks and interpretation

Analytic crossing points; low-mu clean limit; high-mu dense limit.

The root pytest suite supplies numerical, physical and limiting-case checks. Compare floating-point values with tolerances, not byte-for-byte JSON equality; software versions and scheduler IDs are provenance, not numerical targets. The result and analysis identify the model and its limits.
