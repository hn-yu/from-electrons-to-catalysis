# Nudged elastic band

Implement NEB before comparing with ASE.

## Before computing

Forward MB barrier roughly 0.8–1.2 eV; two implementations agree within 0.03 eV. Medium confidence.

This prediction was recorded before the example run. Results and diagnoses are appended in [output/analysis.md](output/analysis.md); do not rewrite the prediction to match the output.

## Implement it

1. Relax endpoints independently.
2. Construct improved tangents and projected forces.
3. Converge a FIRE band and compare ASE using identical potential and spring.
4. Inspect image spacing and increase image count.

Read [hints](hints/README.md) progressively, then inspect the reference implementation in `src/catalysis/` (experiment `neb` in `experiments.py`). Shared algorithms are reused by later projects.

## Run from repository root

```bash
python 05_kinetics/04_neb/run.py
# On a Slurm cluster:
sbatch scripts/slurm.sh 05_kinetics/04_neb/run.py
```

Dependency tier: **core**. See root installation instructions. Input: [input/example.json](input/example.json). Reference result: [output/result.json](output/result.json). Runs default to `runs/04_neb/`, so examples are not overwritten. To reproduce elsewhere, pass `--output PATH`.

## Checks and interpretation

Fixed stationary endpoints; NEB residual; independent ASE barrier.

The root pytest suite supplies numerical, physical and limiting-case checks. Compare floating-point values with tolerances, not byte-for-byte JSON equality; software versions and scheduler IDs are provenance, not numerical targets. The result and analysis identify the model and its limits.
