# Atomic continuation: H on a fixed Cu(111) substrate

The climbing-image ASE/EMT band gives a 0.009493 eV fcc-to-hcp barrier. Both endpoint residual forces are below 0.001 eV/A, and the endpoints remain spatially distinct. The pre-run prediction of a positive barrier below 1 eV is met, though the very broad range has little quantitative predictive power.

The neighboring hollow-site energies are nearly degenerate in this model and the bridge is only slightly higher. Inspect `image-00.extxyz` through `image-08.extxyz` rather than inferring the hop from initial labels alone. The substrate is frozen and the calculator is EMT, so this result tests atomic NEB workflow mechanics and does not claim a physical PBE diffusion barrier.

Numerical agreement of two MB bands was established before this continuation. A subsequent real diffusion study would require converged slab settings, stable physical endpoint states, and checks on substrate relaxation and competing hops.
