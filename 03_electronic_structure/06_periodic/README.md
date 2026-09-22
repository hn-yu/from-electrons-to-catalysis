# Periodic equation of state

Fit a bulk observable and establish a periodic DFT convergence protocol.

## Before computing

EMT Al equilibrium a is 3.8–4.2 A and bulk modulus positive; high confidence. DFT a 3.9–4.2 A, medium confidence.

This prediction was recorded before the example run. Results and diagnoses are appended in [output/analysis.md](output/analysis.md); do not rewrite the prediction to match the output.

## Implement it

1. Run EMT to debug volume per atom and fitting units.
2. Run input/dft.json using GPAW.
3. Vary cutoff, k mesh, smearing and sampled cells; compare lattice constant and modulus.

Read [hints](hints/README.md) progressively, then inspect the reference implementation in `src/catalysis/` (experiment `periodic` in `experiments.py`). Shared algorithms are reused by later projects.

## Run from repository root

```bash
python 03_electronic_structure/06_periodic/run.py
# On a Slurm cluster:
sbatch scripts/slurm.sh 03_electronic_structure/06_periodic/run.py
```

Dependency tier: **core**. See root installation instructions. Input: [input/example.json](input/example.json). Reference result: [output/result.json](output/result.json). Runs default to `runs/06_periodic/`, so examples are not overwritten. To reproduce elsewhere, pass `--output PATH`.

## Checks and interpretation

EOS minimum inside scan; positive modulus; denser volume scan stability.

The root pytest suite supplies numerical, physical and limiting-case checks. Compare floating-point values with tolerances, not byte-for-byte JSON equality; software versions and scheduler IDs are provenance, not numerical targets. The result and analysis identify the model and its limits.

The executed periodic PBE example is in [output/dft/result.json](output/dft/result.json), with a [measured convergence audit](output/dft/analysis.md). It includes separate cutoff, k-point, smearing and volume-sampling variations. The EMT default remains a cheap fitting test.

The next k-mesh refinement was predicted separately and executed with `input/dft_refined.json`. Its [result and prospective tolerance assessment](output/dft_refined/analysis.md) are retained, including either passing or failed observable thresholds.
