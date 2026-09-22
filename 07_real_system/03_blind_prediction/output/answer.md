# Worked analysis: Blind prediction

Observable: PBE H/Cu(111) adsorption relative to half H2. Range: -0.8 to +0.3 eV at the stated high coverage; low confidence. Physical reason: dissociating half a strong H2 bond offsets H–metal bonding; lateral interactions can shift the result. Falsifier: energy outside range, desorption, or a change of sign larger than the numerical uncertainty. This is a deliberately broad teaching prediction and not a literature value. See git history for the pre-run version.

## Postmortem appended after partial results

The unchanged range was -0.8 to +0.3 eV, with low confidence. The three-layer baseline gave approximately +0.046 eV; four layers gave approximately -0.302 eV at the same nominal coverage. Both are within the deliberately broad prediction interval, but their sign disagreement and approximately 0.35 eV difference defeat a claim of a numerically established adsorption sign. A broad interval can be calibrated yet scientifically insufficient. The next prediction should target the layer-convergence trend, rather than merely repeat the broad adsorption range. Full measured results are retained in the real-system project.
