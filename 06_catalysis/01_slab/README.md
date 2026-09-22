# Converge a slab observable

Converge adsorption energy, including matching references.

## Before computing

EMT H adsorption is exothermic relative to half H2; magnitude within 2 eV. Low confidence; this is a workflow test.

This prediction was recorded before the example run. Results and diagnoses are appended in [output/analysis.md](output/analysis.md); do not rewrite the prediction to match the output.

## Implement it

1. Construct Cu(111) and freeze bottom layers.
2. Relax clean and adsorbed slabs and H2 reference.
3. Vary thickness, lateral size, vacuum and relaxation depth.
4. Use GPAW input for electronic convergence axes.

Read [hints](hints/README.md) progressively, then inspect the reference implementation in `src/catalysis/` (experiment `slab` in `experiments.py`). Shared algorithms are reused by later projects.

## Run from repository root

```bash
python 06_catalysis/01_slab/run.py
# On a Slurm cluster:
sbatch scripts/slurm.sh 06_catalysis/01_slab/run.py
```

Dependency tier: **core**. See root installation instructions. Input: [input/example.json](input/example.json). Reference result: [output/result.json](output/result.json). Runs default to `runs/01_slab/`, so examples are not overwritten. To reproduce elsewhere, pass `--output PATH`.

## Checks and interpretation

Relaxed residual forces; exact adsorption energy bookkeeping; target-based tolerance flag.

The root pytest suite supplies numerical, physical and limiting-case checks. Compare floating-point values with tolerances, not byte-for-byte JSON equality; software versions and scheduler IDs are provenance, not numerical targets. The result and analysis identify the model and its limits.
