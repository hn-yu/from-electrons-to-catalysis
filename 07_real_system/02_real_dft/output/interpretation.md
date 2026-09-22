# Interpreting this worked DFT bringup

The initial 1×1×3 Cu(111) slab with one H is a 1 ML model. It is a deliberately small bringup case, not a converged dilute-adsorption reference. The electronic reference is the separately relaxed H2 molecule, and the reported observable is per adsorbed H.

All calculations use PBE and PAW datasets from the installed GPAW data package. Initial slab point-group symmetry is disabled for geometry optimization so small relaxations cannot invalidate the original symmetry reduction. The slab and adsorbate are neutral; a non-spin-polarized metallic state is assumed. A competing magnetic/state search is outside the claim of this Cu/H teaching case.

The calculation separates six assertions:

1. **SCF converged:** GPAW returned energies and forces without an SCF error.
2. **Geometry converged:** each optimizer met its stated maximum movable-force threshold.
3. **Numerically converged:** the actual target-energy sweep must satisfy its tolerance. Here thickness sensitivity already invalidates this assertion for the initial slab.
4. **State physically sensible:** inspect final H coordinates and surface structure. A force-converged symmetry point need not be a minimum in every physical degree of freedom.
5. **Model appropriate:** 0 K PBE, finite slab, coverage, fixed layers and absent solvent must match the intended question. Changing the lateral cell at one H changes the physical coverage.
6. **Claim supported:** the present scan does not justify a coverage-independent or finite-temperature statement about favorable H adsorption, and certainly not a catalytic rate.

The cheapest next step is a same-coverage layer sequence beyond four layers, followed by k-point checks on that thicker slab. Only after the target difference is stable should one compare other sites at common settings and add vibrational and gas chemical-potential terms. This order follows the observed failure, rather than assuming a large calculation automatically resolves it.
