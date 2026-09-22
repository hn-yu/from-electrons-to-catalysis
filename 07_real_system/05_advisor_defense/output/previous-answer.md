# Worked analysis: The internal-advisor defense

First define the claim: accessible microscopic pathway, dominant pathway, or measurable diffusion coefficient? NEB addresses a minimum-energy path between specified metastable endpoints. Verify both endpoints are local minima with compatible stoichiometry, charge and boundary conditions. At finite temperature their populations, entropy, prefactors and recrossing matter. Competing trapping states, desorption and alternative paths can dominate. Translate the observation timescale into a temperature-specific barrier range with the TST calculator. The cheapest falsification is often endpoint relaxation and competing-state energy, before optimizing a path. A smooth converged band neither proves global path optimality nor an experimental mechanism. To support diffusion, include hop lengths, dimensionality, site connectivity, occupancy and correlated hops; to support catalysis, add a reaction network and chemical potentials.

## Define the claim and decision

“X migrates through Y” can mean that a path exists on a chosen potential-energy surface, that Y is the fastest microscopic hop, that migration happens during an experiment, or that it controls catalytic turnover. These claims require different observables. Before calculating, state which decision would change if the barrier were 0.2 eV larger. If no decision changes, precision on this barrier may not be the immediate need.

For an elementary hop the natural observables are endpoint free energies, a conditional escape rate, and competing escape rates. For macroscopic diffusion one additionally needs site connectivity, hop vectors, occupancy, correlation factors and the dimensionality of the random walk. For catalytic activity, migration can be irrelevant if another elementary event limits flux or the migrating species is scarcely populated.

## Establish endpoint states

Relax both endpoints at compatible stoichiometry, charge, spin and boundary conditions. Verify stationary forces and local curvature in the relevant movable degrees of freedom. If the destination relaxes back to the initial site, a band connecting the supplied drawings does not connect two metastable states. Examine several initial spin/adsorbate orientations if the physical system admits them. A small residual on a symmetry-constrained structure can conceal a saddle in a symmetry-breaking direction.

The periodic cell must support the intended displacement without an unintended shorter hop through a boundary. Check whether increasing the cell changes coverage, the identity of the state, or just image interactions. Keep these effects separate when interpreting a convergence sweep. Define which slab atoms are allowed to relax and whether freezing them suppresses a collective path.

## Choose the cheapest falsification

First relax the endpoints and a cheap competing trap or desorbed state. If the starting species is thermodynamically inaccessible at the stated chemical potentials, refine its population before the path. If a competing escape is already much faster on a crude model, a high-precision band along Y may have little explanatory value. Use the toy path and force checker to debug signs and image handling before spending DFT time.

An initial coarse band can identify a likely transition region. Refine the number and placement of images, initialize alternative paths, then use a climbing image or saddle refinement and inspect the unstable mode. A converged band can follow a local path with an unnecessarily high saddle. Multiple initial paths are evidence about path dependence; a single smooth curve is not proof of global optimality.

## Put the barrier on an experimental timescale

For a single populated state, Eyring theory gives k=(kBT/h) exp(-deltaG‡/kBT), assuming a specified dividing surface and transmission coefficient one. For a waiting time tau, invert this relation: deltaG‡=kBT ln[(kBT/h) tau]. Use this only when the logarithm is meaningful for the target timescale. The potential-energy barrier from NEB lacks vibrational/configurational entropy and any reservoir contribution associated with changing state composition.

Compare the resulting rate to competing hops, reaction, trapping and desorption, and compare the expected event count to trajectory length or experimental observation time. A 1 ps trajectory cannot exclude a process with a microsecond waiting time. Conversely, many events in a biased trajectory do not directly measure an unbiased rate without a valid dynamical reweighting method.

## Identify hidden finite-temperature physics

A minimum-energy path minimizes energy over coordinates; a free-energy profile integrates the Boltzmann weight over coordinates omitted from the collective variable. The width of the accessible transverse basin can change the free-energy barrier even if the path energies do not change. Slow hidden coordinates can make a reconstructed profile depend on the starting state. Use independent starts, overlap diagnostics and an alternative collective variable to look for this failure.

An experimental apparent activation energy is a slope of the total observable with inverse temperature. It can include changes in coverage, selectivity, mechanism or transport and need not equal one elementary barrier. A microkinetic sensitivity calculation that preserves detailed balance is a more defensible way to connect elementary uncertainty to turnover than naming the largest isolated barrier the rate-determining step.

## What the result would and would not establish

A carefully converged NEB establishes a candidate path and barrier within its potential, boundary conditions and endpoint definitions. It does not by itself establish that the endpoints are populated, that competing paths are absent, that the functional describes the electronic state, or that the experimental observable is controlled by this motion. Supporting a mechanism requires showing that its predicted observables survive reasonable state, numerical and model changes and outperform plausible alternatives.

The next calculation should address the weakest inference in that chain: endpoint population, alternate path, entropy, spin state or sensitivity of the full network. The stopping criterion is sufficient evidence for the stated decision, not the prettiest path plot or the largest computation.
