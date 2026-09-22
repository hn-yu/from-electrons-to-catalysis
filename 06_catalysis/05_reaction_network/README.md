# Detailed-balance reaction network

Represent a three-step reversible catalytic cycle.

## Before computing

Log detailed-balance residual near machine precision; high confidence.

This prediction was recorded before the example run. Results and diagnoses are appended in [output/analysis.md](output/analysis.md); do not rewrite the prediction to match the output.

## Implement it

1. Define free energies, transition states and stoichiometry.
2. Derive forward and reverse barriers from shared states.
3. Check local detailed balance and site conservation.

Read [hints](hints/README.md) progressively, then inspect the reference implementation in `src/catalysis/` (experiment `reaction_network` in `experiments.py`). Shared algorithms are reused by later projects.

## Run from repository root

```bash
python 06_catalysis/05_reaction_network/run.py
# On a Slurm cluster:
sbatch scripts/slurm.sh 06_catalysis/05_reaction_network/run.py
```

Dependency tier: **core**. See root installation instructions. Input: [input/example.json](input/example.json). Reference result: [output/result.json](output/result.json). Runs default to `runs/05_reaction_network/`, so examples are not overwritten. To reproduce elsewhere, pass `--output PATH`.

## Checks and interpretation

Detailed balance; column site balance; equilibrium cycle product.

The root pytest suite supplies numerical, physical and limiting-case checks. Compare floating-point values with tolerances, not byte-for-byte JSON equality; software versions and scheduler IDs are provenance, not numerical targets. The result and analysis identify the model and its limits.

## Explicit reaction and standard-state convention

The implemented cycle is:

```text
A(g) + *  <=> A*
A*        <=> B*
B*        <=> B(g) + *
```

The surface state vector is `[vacancy, A*, B*]`, whose fractions sum to one. Gas species are chemostatted reservoirs, with dimensionless activities `pA/1 bar` and `pB/1 bar`. The `states_eV` entries refer to vacancy+A(g), A*, and B*; `product_eV` refers to vacancy+B(g). A shared transition-state energy gives both directions of each step. Rates are `kf0*aA*theta_v-kr0*theta_A`, `kf1*theta_A-kr1*theta_B`, and `kf2*theta_B-kr2*aB*theta_v`.

At reservoir equilibrium, `aB/aA=exp(-product_eV/kBT)` because the initial standard-state energy is zero. This must give zero cycle flux. The next project solves this exact same network. Its linear generator allows an independent matrix-exponential/BDF check without requiring Cantera; more general networks with lateral interactions or multiple site types need a nonlinear solver and additional validation.
