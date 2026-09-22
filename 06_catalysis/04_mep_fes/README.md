# MEP versus free energy

Integrate a transverse harmonic coordinate analytically.

## Before computing

F barrier decreases with temperature because transverse entropy favors the saddle region; high confidence.

This prediction was recorded before the example run. Results and diagnoses are appended in [output/analysis.md](output/analysis.md); do not rewrite the prediction to match the output.

## Implement it

1. Minimize over y to obtain the 0 K path.
2. Integrate over y to obtain the T-dependent entropy.
3. Find the shifted free-energy minima and barrier.

Read [hints](hints/README.md) progressively, then inspect the reference implementation in `src/catalysis/` (experiment `mep_fes` in `experiments.py`). Shared algorithms are reused by later projects.

## Run from repository root

```bash
python 06_catalysis/04_mep_fes/run.py
# On a Slurm cluster:
sbatch scripts/slurm.sh 06_catalysis/04_mep_fes/run.py
```

Dependency tier: **core**. See root installation instructions. Input: [input/example.json](input/example.json). Reference result: [output/result.json](output/result.json). Runs default to `runs/04_mep_fes/`, so examples are not overwritten. To reproduce elsewhere, pass `--output PATH`.

## Checks and interpretation

Zero-temperature recovery; barrier temperature trend; symmetric profiles.

The root pytest suite supplies numerical, physical and limiting-case checks. Compare floating-point values with tolerances, not byte-for-byte JSON equality; software versions and scheduler IDs are provenance, not numerical targets. The result and analysis identify the model and its limits.
