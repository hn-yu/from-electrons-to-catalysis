# Measured result and postmortem

LJ dimer energy span: 1.8e-05 reduced units. Harmonic dt=2.01 gives final energy 1.57e+51, confirming loss of stability above dt=2. Stable timestep errors scale quadratically; bounded oscillation alone is not sampling convergence.

Input SHA-256: `d49175c0e44774f8f333f7e738157eb69b1722796decf2bfa2929a7d8dccc53a`. Slurm job: `705307`. Software versions and source revision are in [result.json](result.json).

Predictions remain unchanged in the project README and root predictions.md. Numerical agreement validates the stated model and checks, not an unrestricted scientific claim.
