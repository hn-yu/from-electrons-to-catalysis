# Molecular thermochemistry

Obtain frequencies and build independent RRHO thermochemistry.

## Before computing

All optimized internal frequencies positive; ASE G agreement <1e-4 eV; gas entropy exceeds vibrational entropy alone. High confidence.

This prediction was recorded before the example run. Results and diagnoses are appended in [output/analysis.md](output/analysis.md); do not rewrite the prediction to match the output.

## Implement it

1. Optimize four molecules with RHF gradients.
2. Mass-weight the analytic Hessian and project translations/rotations.
3. Combine translational, rotational, vibrational and electronic contributions.
4. Compare G against ASE IdealGasThermo.

Read [hints](hints/README.md) progressively, then inspect the reference implementation in `src/catalysis/` (experiment `molecular_thermo` in `experiments.py`). Shared algorithms are reused by later projects.

## Run from repository root

```bash
python 04_thermodynamics/02_molecular_thermochemistry/run.py
# On a Slurm cluster:
sbatch scripts/slurm.sh 04_thermodynamics/02_molecular_thermochemistry/run.py
```

Dependency tier: **quantum**. See root installation instructions. Input: [input/example.json](input/example.json). Reference result: [output/result.json](output/result.json). Runs default to `runs/02_molecular_thermochemistry/`, so examples are not overwritten. To reproduce elsewhere, pass `--output PATH`.

## Checks and interpretation

Stationary geometry; correct mode count; independently assembled G versus ASE.

The root pytest suite supplies numerical, physical and limiting-case checks. Compare floating-point values with tolerances, not byte-for-byte JSON equality; software versions and scheduler IDs are provenance, not numerical targets. The result and analysis identify the model and its limits.

## Thermochemical model

The calculation uses optimized gas-phase RHF/STO-3G geometries and harmonic frequencies, an ideal translational partition function, and the high-temperature rigid-rotor approximation. All four molecules are closed-shell singlets. Rotational symmetry numbers are specified in the input; nuclear-spin ortho/para statistics, anharmonicity and hindered rotors are omitted. The pressure standard is 1 bar, and no solution-phase concentration conversion is made. The small residual against ASE measures implementation agreement for this shared RRHO model, not accuracy against experimental spectra or entropies.
