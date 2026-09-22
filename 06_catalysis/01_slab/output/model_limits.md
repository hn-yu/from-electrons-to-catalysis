# What the EMT convergence check establishes

EMT has no k points, plane-wave cutoff or electronic smearing. The default sweep therefore tests only the structural workflow and finite-range potential. In this run the largest change among tested axes is about 0.00053 eV, but that is not evidence of DFT slab convergence.

The real PBE counterpart is [section 7's complete sweep](../../../07_real_system/02_real_dft/output/result.json). There, thickness and electronic sampling can materially affect adsorption energy. The separate `input/dft.json` extends this chapter's 2×2 slab workflow to GPAW; its full sweep is an additional exercise, not mislabeled as having been executed by the EMT reference.

The lateral-cell variation changes the adsorbate coverage because the number of H atoms is fixed at one. Treat that axis as a combined finite-size/coverage study. A same-coverage finite-size comparison must replicate the adsorbates along with the surface cell.
