# Write restricted Hartree-Fock

Use PySCF only for integrals and a reference; implement the SCF loop.

## Before computing

H2 energy near -1.117 Eh; all three independent loops match PySCF within 1e-7 Eh. High confidence; any larger residual falsifies implementation.

This prediction was recorded before the example run. Results and diagnoses are appended in [output/analysis.md](output/analysis.md); do not rewrite the prediction to match the output.

## Implement it

1. Build S, h and electron repulsion integrals.
2. Construct J and K with a spin-summed density.
3. Add DIIS and converge energy, density and commutator.
4. Compare all three molecules against PySCF RHF.

Read [hints](hints/README.md) progressively, then inspect the reference implementation in `src/catalysis/` (experiment `scf` in `experiments.py`). Shared algorithms are reused by later projects.

## Run from repository root

```bash
python 03_electronic_structure/03_rhf/run.py
# On a Slurm cluster:
sbatch scripts/slurm.sh 03_electronic_structure/03_rhf/run.py
```

Dependency tier: **quantum**. See root installation instructions. Input: [input/example.json](input/example.json). Reference result: [output/result.json](output/result.json). Runs default to `runs/03_rhf/`, so examples are not overwritten. To reproduce elsewhere, pass `--output PATH`.

## Checks and interpretation

Reference energy; electron count; stable stationary density.

The root pytest suite supplies numerical, physical and limiting-case checks. Compare floating-point values with tolerances, not byte-for-byte JSON equality; software versions and scheduler IDs are provenance, not numerical targets. The result and analysis identify the model and its limits.
