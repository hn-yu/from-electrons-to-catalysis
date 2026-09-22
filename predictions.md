# Pre-computation prediction register

Entries below are teaching predictions recorded before running the new implementations. The existing Hamiltonian note is preserved. Measured outcomes are appended in each project output/analysis.md.

## 02_bringup/01_units

kBT is about 0.026, 0.052, 0.086, 0.129 eV; high confidence from linear scaling. Falsifier: >2% discrepancy.

Reason and model: Convert numbers into physical scales. The stated checks are the falsification criteria: Round trips; linear temperature scaling; incompatible dimensions rejected.

## 02_bringup/02_forces

Force vanishes at 0.74 A; compressed bonds repel and stretched bonds attract. Error <1e-6 eV/A; high confidence.

Reason and model: Implement and validate the sign and units of an analytic force. The stated checks are the falsification criteria: Analytic/finite difference agreement; force sign; dissociation limit.

## 02_bringup/03_finite_differences

The best h lies between 1e-7 and 1e-4 A; errors rise at both extremes. Medium confidence; falsified by monotonic error.

Reason and model: Expose cancellation and truncation error. The stated checks are the falsification criteria: Interior error minimum; correct force sign; large-step versus tiny-step error.

## 03_electronic_structure/01_schrodinger

Harmonic energies start at 0.5 Eh; states have 0,1,2,3 nodes; double well has a small positive splitting. High confidence.

Reason and model: Construct a finite-difference Hamiltonian in atomic units. The stated checks are the falsification criteria: Box analytic spectrum; oscillator zero-point energy; grid normalization and ordering.

## 03_electronic_structure/02_lcao

Energies are approximately -1.0833 and -0.875 Eh; lower eigenvector is bonding. High confidence.

Reason and model: Solve Hc=ESc without pretending an AO basis is orthogonal. The stated checks are the falsification criteria: Generalized residual; S orthogonality; zero-overlap limit and variational upper bound.

## 03_electronic_structure/03_rhf

H2 energy near -1.117 Eh; all three independent loops match PySCF within 1e-7 Eh. High confidence; any larger residual falsifies implementation.

Reason and model: Use PySCF only for integrals and a reference; implement the SCF loop. The stated checks are the falsification criteria: Reference energy; electron count; stable stationary density.

## 03_electronic_structure/04_break_hf

At 5 A UHF lies substantially below RHF and S^2 tends toward 1; high confidence. Triplet O2 expected lower, medium confidence.

Reason and model: Separate basis, spin, convergence and correlation failures. The stated checks are the falsification criteria: SCF convergence; UHF variational energy; correct singlet S^2 near equilibrium.

## 03_electronic_structure/05_dft

FCI <= RHF; the difference grows on stretching. Functionals disagree despite SCF convergence; high confidence.

Reason and model: Compare approximations at identical geometry and basis. The stated checks are the falsification criteria: FCI variational ordering; repeatable functional energies; stretched versus equilibrium correlation error.

## 03_electronic_structure/06_periodic

EMT Al equilibrium a is 3.8–4.2 A and bulk modulus positive; high confidence. DFT a 3.9–4.2 A, medium confidence.

Reason and model: Fit a bulk observable and establish a periodic DFT convergence protocol. The stated checks are the falsification criteria: EOS minimum inside scan; positive modulus; denser volume scan stability.

## 04_thermodynamics/01_partition

Excited population rises toward 3/4; oscillator U tends to 0.06 eV at low T. High confidence.

Reason and model: Derive entropy from state counting. The stated checks are the falsification criteria: Population normalization; U-F=TS; high/low-temperature limits.

## 04_thermodynamics/02_molecular_thermochemistry

All optimized internal frequencies positive; ASE G agreement <1e-4 eV; gas entropy exceeds vibrational entropy alone. High confidence.

Reason and model: Obtain frequencies and build independent RRHO thermochemistry. The stated checks are the falsification criteria: Stationary geometry; correct mode count; independently assembled G versus ASE.

## 04_thermodynamics/03_chemical_potential

Adsorption deltaE=-0.6 eV but deltaG>0 at 1000 K and 1 bar; high confidence.

Reason and model: Show why favorable adsorption energy need not imply favorable free energy. The stated checks are the falsification criteria: p=p0 identity; logarithmic pressure slope; unfavorable low-pressure limit.

## 04_thermodynamics/04_surface_phase

Clean→quarter→half transitions at mu=-0.5 and -0.2 eV; high confidence.

Reason and model: Take the lower envelope of surface grand potentials. The stated checks are the falsification criteria: Analytic crossing points; low-mu clean limit; high-mu dense limit.

## 05_kinetics/01_optimizer

Morse converges to 0.74 A; MB starts find at least two minima. High confidence.

Reason and model: Find local minima using steepest descent and backtracking. The stated checks are the falsification criteria: Small residual forces; Morse exact minimum; multiple basins.

## 05_kinetics/02_dynamics

Error scales approximately as dt^2 in stable regime; dt>2 fails. High confidence.

Reason and model: Separate timestep error from sampling and physical timescales. The stated checks are the falsification criteria: Energy error scaling; momentum conservation; harmonic stability boundary.

## 05_kinetics/03_hessian

MB minimum has zero negative modes; saddle has exactly one. High confidence.

Reason and model: Classify stationary points through curvature. The stated checks are the falsification criteria: Hessian symmetry; minimum/saddle inertia; Morse analytic curvature.

## 05_kinetics/04_neb

Forward MB barrier roughly 0.8–1.2 eV; two implementations agree within 0.03 eV. Medium confidence.

Reason and model: Implement NEB before comparing with ASE. The stated checks are the falsification criteria: Fixed stationary endpoints; NEB residual; independent ASE barrier.

## 05_kinetics/05_tst

A 1 eV barrier is very slow at 300 K and much faster at 1000 K; high confidence.

Reason and model: Turn a free-energy barrier into a conditional rate estimate. The stated checks are the falsification criteria: Zero-barrier prefactor; monotonic barrier dependence; inverse rate timescale.

## 06_catalysis/01_slab

EMT H adsorption is exothermic relative to half H2; magnitude within 2 eV. Low confidence; this is a workflow test.

Reason and model: Converge adsorption energy, including matching references. The stated checks are the falsification criteria: Relaxed residual forces; exact adsorption energy bookkeeping; target-based tolerance flag.

## 06_catalysis/02_adsorption

Hollow sites likely below atop for this toy EMT setup; low confidence. Falsifier: optimized ordering reverses.

Reason and model: Compare symmetry-distinct initial adsorption sites. The stated checks are the falsification criteria: Energy reference; force convergence; final-site inspection.

## 06_catalysis/03_umbrella

WHAM shape error <0.03 eV; adjacent windows overlap; hidden high-barrier y retains its initial sign. Medium confidence.

Reason and model: Reconstruct an unbiased free-energy profile and reveal bad coordinates. The stated checks are the falsification criteria: WHAM self-consistency; exact marginal comparison; overlap and independent-start diagnostic.

## 06_catalysis/04_mep_fes

F barrier decreases with temperature because transverse entropy favors the saddle region; high confidence.

Reason and model: Integrate a transverse harmonic coordinate analytically. The stated checks are the falsification criteria: Zero-temperature recovery; barrier temperature trend; symmetric profiles.

## 06_catalysis/05_reaction_network

Log detailed-balance residual near machine precision; high confidence.

Reason and model: Represent a three-step reversible catalytic cycle. The stated checks are the falsification criteria: Detailed balance; column site balance; equilibrium cycle product.

## 06_catalysis/06_microkinetics

Coverages positive and sum to 1; steady TOF positive; integrated and algebraic populations agree to 1e-6. High confidence.

Reason and model: Solve site populations and compare a direct steady state with time integration. The stated checks are the falsification criteria: ODE/direct agreement; site conservation; zero TOF at thermodynamic equilibrium.

## 06_catalysis/07_rate_control

The largest isolated forward barrier need not have largest DRC; medium confidence. Falsifier: this input gives the same ranking.

Reason and model: Distinguish isolated barriers from control over flux. The stated checks are the falsification criteria: Detailed balance after perturbation; DRC sum near 1; nonlinear ±0.1 eV response.

## 07_real_system/02_real_dft

PBE H/Cu(111) adsorption relative to half H2 expected -0.8 to +0.3 eV; low confidence. Falsifier: outside range or unstable final adsorption geometry.

Reason and model: Carry one H/Cu(111) adsorption subproblem through an explicit DFT convergence audit. The stated checks are the falsification criteria: Relaxed forces; matching H2 and slab references; all numerical axes versus 0.05 eV.

