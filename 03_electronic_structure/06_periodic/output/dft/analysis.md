# PBE Al equation of state: measured convergence audit

GPAW/PBE gives an equilibrium lattice constant of 4.047677 A and bulk modulus of 80.537 GPa at 250 eV, a 4×4×4 k mesh and 0.1 eV smearing. This lies inside the recorded 3.9–4.2 A prediction.

| Change from baseline | a0 (A) | B (GPa) |
|---|---:|---:|
| 300 eV cutoff | 4.047614 | 80.498 |
| 6×6×6 k mesh | 4.042047 | 79.458 |
| 0.05 eV smearing | 4.047551 | 80.873 |
| Denser volume sampling | 4.047783 | 80.884 |

The k-mesh effect is larger than the sampled cutoff effect. For a **proposed next-run tolerance** of 0.005 A and 2 GPa, the sampled k-mesh change fails the lattice-constant criterion. These thresholds are a post-run diagnostic, not retroactively claimed pre-run targets. The next cheapest calculation is a denser k mesh at the same cutoff and volume grid. A converged SCF at each volume does not by itself converge the fitted observable.

These are periodic PBE calculations, distinct from the EMT default example. `result.json` retains every input and fitted scan. Atomic volumes use a primitive fcc cell with V=a³/4; the fit is Birch–Murnaghan. This small mesh study does not establish an asymptotic convergence plateau.
