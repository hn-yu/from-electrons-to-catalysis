# Break Hartree-Fock

Separate basis, spin, convergence and correlation failures.

## Before computing

At 5 A UHF lies substantially below RHF and S^2 tends toward 1; high confidence. Triplet O2 expected lower, medium confidence.

This prediction was recorded before the example run. Results and diagnoses are appended in [output/analysis.md](output/analysis.md); do not rewrite the prediction to match the output.

## Implement it

1. Stretch H2 with an explicitly broken-spin UHF guess.
2. Compare nominal singlet and triplet O2.
3. Sweep H2 basis size at a fixed geometry.

Read [hints](hints/README.md) progressively, then inspect the reference implementation in `src/catalysis/` (experiment `hf_failures` in `experiments.py`). Shared algorithms are reused by later projects.

## Run from repository root

```bash
python 03_electronic_structure/04_break_hf/run.py
# On a Slurm cluster:
sbatch scripts/slurm.sh 03_electronic_structure/04_break_hf/run.py
```

Dependency tier: **quantum**. See root installation instructions. Input: [input/example.json](input/example.json). Reference result: [output/result.json](output/result.json). Runs default to `runs/04_break_hf/`, so examples are not overwritten. To reproduce elsewhere, pass `--output PATH`.

## Checks and interpretation

SCF convergence; UHF variational energy; correct singlet S^2 near equilibrium.

The root pytest suite supplies numerical, physical and limiting-case checks. Compare floating-point values with tolerances, not byte-for-byte JSON equality; software versions and scheduler IDs are provenance, not numerical targets. The result and analysis identify the model and its limits.
