## From Electrons to Catalysis

Modern computational chemistry education often teaches software recipes faster than physical judgment. It is easy to learn how to launch a DFT calculation and much harder to know whether the calculation answers the scientific question, whether the result has the right order of magnitude, and what the cheapest falsifying calculation should be.

This is a rough outline for a **12 week course** that tries to build that judgment from first principles. The structure is inspired by George Hotz's [From the Transistor to the Web Browser](https://github.com/geohot/fromthetransistor): every project builds on the previous ones, small transparent implementations come before production libraries, and the course ends by running the whole stack on a real problem.

Project annotations use the form **(language/tool, approximate LOC, estimated focused hours)**. `LOC` means approximate lines of source code, not minutes. The hour estimate includes implementation, numerical/physical checks, and a short write-up, but excludes optional background reading and the wall-clock/queue time of production DFT jobs. The full course is roughly **135–150 hours of focused work**, or about **11–13 hours/week**.

The stack we want to understand is:

```text
Hamiltonian
    ↓
electronic structure
    ↓
potential-energy surface
    ↓
forces and dynamics
    ↓
statistical mechanics
    ↓
free energy
    ↓
reaction rates
    ↓
reaction network
    ↓
experimental observables
```

The goal is not to memorize computational chemistry. The goal is to develop an **internal advisor**: given a new idea, you should be able to predict the relevant scale, choose an observable, identify the approximations, design numerical and physical unit tests, and decide what result would falsify the idea before spending serious compute.

All projects should build on each other. Keep one repository and reuse the code you write. Do not throw away the toy implementation when a library version appears later; the library is the reference implementation you test yourself against.

#### Section 1: Intro: Cheating our way past the many-body Schrödinger equation -- 0.5 weeks

- **So about that Hamiltonian (notes, —, 1.5–2 h)** -- Course overview. Write down the electron+nuclei Hamiltonian and identify kinetic, electron-electron, electron-nuclear, and nuclear-nuclear terms. Explain what the Born-Oppenheimer approximation buys us and why a potential-energy surface can exist. Briefly locate Hartree-Fock, density-functional theory, correlated wave-function methods, statistical mechanics, transition-state theory, molecular dynamics, and microkinetics in the approximation stack. We cannot build an exact many-electron solver, so we will cheat deliberately and keep track of where we cheat.
- **Emulation (setup/notes, —, 0.5–1 h)** -- Real catalytic systems are terrible teaching systems: too many atoms, magnetic states, reconstructions, collective variables, and numerical choices can all fail at once. Most of the course therefore uses two-level systems, Morse potentials, the Müller-Brown potential, small molecules, simple crystals, and simple surfaces. These are the equivalent of an emulator: small enough that a wrong intuition can be diagnosed. Production DFT is postponed until the lower layers are understood.
- **The prediction log (Markdown, ~30 LOC, 0.5 h)** -- Create `predictions.md`. Before every numerical experiment record: prediction, plausible range, confidence, reason, and what observation would falsify the prediction. Never edit the prediction after seeing the result. Add a postmortem instead.

#### Section 2: Bringup: What does a calculation actually return? -- 0.5 weeks

- **Building a units and scales module (Python, ~100 LOC, 1.5–2 h)** -- Implement eV ↔ kJ/mol, Hartree ↔ eV, cm⁻¹ ↔ eV, bar ↔ Pa, and common time units. Add `kBT(T)`. Without looking anything up, predict `kBT` at 300, 600, 1000, and 1500 K, then test yourself. The objective is to stop seeing `1.0 eV`, `1000 K`, and `1 ps` as abstract numbers.
- **Building an energy/force interface (Python, ~150 LOC, 2–3 h)** -- Implement a Morse potential with `energy(x)` and analytic `force(x)`, then implement a finite-difference force checker. Require the numerical and analytic forces to agree over a scan of bond lengths. This becomes the testing interface reused by the optimizer, molecular dynamics, Hessian, and reaction-path projects later.
- **Breaking finite differences on purpose (Python, ~50 LOC, 1–1.5 h)** -- Sweep the finite-difference displacement over many orders of magnitude. Observe truncation error on one side and floating-point cancellation on the other. Write down why a numerically converged-looking derivative is not automatically a trustworthy derivative.

#### Section 3: Electronic Structure: Where does an energy come from? -- 3 weeks

- **Coding a 1D Schrödinger solver (Python, ~250 LOC, 5–6 h)** -- Discretize `-½ d²/dx² + V(x)` on a grid and diagonalize the Hamiltonian. Solve a particle in a box, harmonic oscillator, finite well, and double well. Reproduce energy ordering, nodes, zero-point energy, and tunneling splitting. Predict the qualitative eigenfunctions before plotting them.
- **Building a minimal LCAO model (Python, ~150 LOC, 3–4 h)** -- Solve the generalized eigenvalue problem `Hc = ESc` for two non-orthogonal basis functions. Understand overlap, bonding and antibonding combinations, the variational principle, and why changing a basis set can change an answer even when the underlying Hamiltonian is unchanged.
- **Building restricted Hartree-Fock SCF (Python + PySCF integrals, ~400 LOC, 8–10 h)** -- Let PySCF provide AO integrals, but write the SCF loop yourself: initial density → Fock matrix → orthogonalization → diagonalization → occupations → new density → convergence. Run H₂, HeH⁺, and LiH. Compare your final energy to PySCF RHF. The point is that `SCF converged` should cease to be a magical message.
- **Breaking Hartree-Fock on purpose (PySCF, ~120 LOC, 3–4 h)** -- Stretch H₂ and compare RHF and UHF. Run O₂ with correct and incorrect spin assumptions. Sweep STO-3G → 6-31G → cc-pVDZ → cc-pVTZ on a small molecule. Separate basis error, method error, spin/state error, and SCF convergence.
- **So about DFT (PySCF, ~150 LOC, 3–4 h)** -- On the same small systems compare HF, LDA, GGA, a hybrid functional, and a correlated wave-function reference where affordable. Do not implement PBE. Instead explain precisely what changes when the basic object becomes the density, what the exchange-correlation functional is responsible for, and why two converged functionals can give meaningfully different chemistry.
- **Periodic bringup (ASE + periodic DFT backend, ~200 LOC, 5–7 h active work)** -- Calculate an equation of state for a simple solid such as Al, Cu, or Si using GPAW, Quantum ESPRESSO, VASP, or another periodic backend. Extract equilibrium lattice parameter and bulk modulus. Deliberately vary cutoff/basis quality, k-point density, smearing, and cell sampling. Define convergence in terms of an **observable and tolerance**, not an input keyword.
- **Electronic-structure checkpoint (written analysis, —, 1 h)** -- Given a calculation that is perfectly SCF-converged, list at least five independent reasons why its scientific conclusion could still be wrong.

#### Section 4: Thermodynamics: Energy is not free energy -- 2 weeks

- **Building a partition function (Python, ~200 LOC, 4–5 h)** -- Start with a two-level system and implement `Z`, populations, internal energy, entropy, and Helmholtz free energy. Add degeneracy. Then implement the harmonic-oscillator partition function. Plot how populations change with temperature. The objective is to see entropy emerge from state counting instead of treating `-TΔS` as an arbitrary correction.
- **Building molecular thermochemistry (Python + PySCF/ASE, ~220 LOC, 5–7 h)** -- For H₂, CO, CO₂, and H₂O obtain vibrational frequencies, then construct electronic energy, zero-point energy, thermal enthalpy, entropy, and Gibbs free energy. Compare your implementation against a trusted thermochemistry library. Explain why gas-phase entropy is often much larger than an adsorbate vibrational entropy.
- **Building chemical potential (Python, ~150 LOC, 2–3 h)** -- Implement the ideal-gas pressure dependence `μ(T,p) = μ°(T) + kBT ln(p/p°)` and plot chemical potentials over experimentally relevant temperature and pressure ranges. Use it in a simple adsorption/reaction equilibrium where the sign of `ΔE` and the sign of `ΔG(T,p)` disagree.
- **Building a surface phase diagram (Python, ~200 LOC, 3–4 h)** -- Given DFT energies for a clean surface and several coverages/states, construct an ab-initio thermodynamics diagram versus chemical potential or `(T,p)`. Identify which assumptions let a handful of 0 K electronic energies become a finite-temperature stability statement.
- **Thermodynamics checkpoint (written analysis, —, 1 h)** -- For any reported `ΔG`, you must be able to name the ensemble, reference states, temperature, pressure/chemical potentials, degrees of freedom included, and degrees of freedom omitted.

#### Section 5: Kinetics: A possible path is not a relevant path -- 2 weeks

- **Building an optimizer (Python, ~150 LOC, 2–3 h)** -- Optimize a Morse potential and the Müller-Brown potential using your force interface. Implement steepest descent; optionally add or wrap BFGS. Start from multiple initial conditions and show that optimization finds a local stationary point, not "the correct structure."
- **Building molecular dynamics (Python, ~220 LOC, 4–5 h)** -- Implement velocity Verlet on the harmonic oscillator and then on a simple many-particle potential. Measure energy drift. Sweep the timestep until the integration fails. Use an ASE thermostat only after the NVE implementation works. Distinguish integration timestep, trajectory length, physical event timescale, and sampling time.
- **Building a Hessian and vibrational analysis (Python, ~180 LOC, 3–4 h)** -- Finite-difference your force function to construct a Hessian. Mass-weight and diagonalize it. Distinguish a minimum from a first-order saddle point and inspect whether an imaginary mode corresponds to the intended reaction coordinate.
- **Building a NEB (Python, ~300 LOC, 6–8 h)** -- Implement a simple elastic-band/NEB-style path optimizer on the 2D Müller-Brown potential, then compare with ASE NEB. Only after that, run a simple atom-diffusion or molecular rearrangement example. Predict the transition-state region and barrier before running it. Learn why metastable endpoints, image spacing, path initialization, optimizer convergence, and hidden degrees of freedom matter.
- **Building a transition-state-theory calculator (Python, ~200 LOC, 2–3 h)** -- Implement Eyring/TST and a simple Arrhenius form. Make a permanent barrier-timescale map for 0–3 eV at 300, 600, 1000, and 1500 K. A barrier should begin to evoke a timescale automatically rather than being judged as "high" or "low" in isolation.
- **Kinetics checkpoint (written analysis, —, 1 h)** -- Given a barrier, refuse to call it kinetically relevant until temperature, prefactor/free-energy treatment, state definition, and competing pathways have been specified.

#### Section 6: Catalysis: From elementary calculations to an observable -- 3 weeks

- **Building and converging a slab (ASE + DFT, ~220 LOC, 5–7 h active work)** -- Construct a simple metal surface such as Cu(111) or Pt(111). Converge slab thickness, vacuum, k-point density, relaxation depth, and lateral cell size against the quantity you actually care about. The test target should be an adsorption energy or reaction energy, not the raw total energy.
- **Adsorbing something (ASE + DFT, ~150 LOC, 4–5 h active work)** -- Place H, O, or CO at several symmetry-distinct sites. Before calculating, rank the sites and give a confidence level and physical reason. After calculating, explain any failed prediction in terms of coordination, orbital interaction, surface relaxation, magnetism where relevant, and coverage rather than simply replacing the prediction with the computed ordering.
- **Building umbrella sampling on a toy system (Python, ~300 LOC, 6–8 h)** -- Sample a double-well potential under harmonic bias windows and reconstruct `F(x) = -kBT ln P(x)` (a simple WHAM implementation is encouraged). Add a hidden coordinate and deliberately choose a bad collective variable. Observe how a plausible-looking one-dimensional free-energy profile can hide slow orthogonal motion.
- **MEP versus FES (Python + analysis, ~120 LOC, 2–3 h)** -- For one toy landscape compare a 0 K minimum-energy path with a finite-temperature free-energy profile. Change temperature. Write a one-page explanation of when a NEB barrier, an umbrella/OPES/metadynamics barrier, and an experimental apparent activation energy are different physical objects.
- **Building a reaction network (Python, ~300 LOC, 4–5 h)** -- Define species, site balances, stoichiometry, `ΔG`, `ΔG‡`, forward/reverse rate constants, and elementary rates. Enforce thermodynamic consistency through detailed balance. Start with a three- or four-step toy catalytic cycle.
- **Building a microkinetic solver (Python, ~500 LOC, 7–9 h)** -- Integrate or directly solve the coverage equations to steady state. Compute coverages, TOF, reaction orders, selectivity where applicable, and apparent activation energy. Sweep temperature and gas pressures. Compare the result to a reference implementation such as Cantera when possible.
- **Breaking the "rate-determining step" intuition (Python, ~150 LOC, 2–3 h)** -- Construct a network in which the highest isolated barrier is not the step with the largest control over TOF. Perturb adsorption/reaction energies by ±0.1 eV and measure the effect on the observable. Implement a finite-difference sensitivity or degree-of-rate-control analysis.
- **Catalysis checkpoint (written analysis, —, 1 h)** -- Starting from one elementary DFT energy, identify every additional modeling layer required before it can legitimately support a statement about activity, selectivity, mechanism, or experiment.

#### Section 7: Physical: Running on a real catalyst -- 1 week

- **Talking to the catalyst (Markdown, ~1 page per calculation, 0.5–1 h each)** -- Before submitting a serious job, write: scientific question; current hypothesis; predicted range; confidence; relevant physics; required observable; model assumptions; numerical failure modes; physical failure modes; cheapest falsifying calculation; and what result would make you abandon the hypothesis. A job without this memo does not run.
- **Real DFT bringup (ASE/VASP/QE/GPAW, project dependent, 8–12 h active work)** -- Choose one real catalytic subproblem and perform the complete numerical bringup appropriate to it: structure/state preparation, spin or charge where relevant, cell/k-points/cutoff, relaxation protocol, reference energies, multiple initial states when needed, and convergence against the target observable. Distinguish `SCF converged`, `geometry converged`, `numerically converged`, `state physically sensible`, `model appropriate`, and `claim supported` as six different assertions.
- **Blind prediction (Markdown, ~0.5 page, 0.5 h)** -- Before seeing the final result, commit a predicted range for the important observable (adsorption energy, reaction energy, barrier, free-energy difference, rate, or trend), plus the physical argument behind the range. Keep the failed predictions. They are the training data for intuition.
- **Bringup (analysis, —, 2–4 h)** -- Run the real calculation, compare it to the prediction, diagnose the discrepancy, identify which assumption failed, and design the next calculation for maximum information gain rather than maximum sophistication.
- **The internal-advisor defense (Markdown, ~2 pages, 3–4 h)** -- Take a proposal such as "species X migrates through pathway Y, so let's run NEB." Without running new calculations, decide what claim is actually being made, whether NEB is the right observable, what the endpoint states must satisfy, what temperature changes, what competing states/pathways could invalidate the interpretation, what barrier range would be kinetically meaningful, what the cheapest falsification is, and what a beautiful-looking result would still fail to prove. The course is passed when this reasoning is more valuable than simply asking which input file to run.

## Project rules

1. **Prediction before computation.** Every nontrivial calculation gets a predicted value/range, confidence, reason, and falsifier before execution.
2. **Build the toy version before using the library.** Implement the transparent core of SCF, partition functions, Verlet, Hessians, NEB, TST, and microkinetics before delegating them to production packages.
3. **Every calculation gets three unit tests.** At minimum: a numerical test, a physical test, and a limiting-case/sanity test.
4. **A converged answer is not a correct answer.** Keep numerical correctness, model correctness, physical correctness, and claim correctness separate.
5. **Use an observable as the convergence target.** Do not converge input parameters in the abstract.
6. **Try to kill the idea cheaply.** The first calculation should maximize information gain, not computational cost.
7. **Every week ends with one reusable rule.** Store it in `judgment.md`. By the end of the course this should become a personal library of physical heuristics and their domains of validity.
8. **Do not erase wrong intuition.** A failed prediction followed by a correct diagnosis is more valuable than an unrecorded correct guess.

## Suggested repository layout

```text
from-electrons-to-catalysis/
├── README.md
├── predictions.md
├── judgment.md
├── 01_intro/
├── 02_bringup/
├── 03_electronic_structure/
├── 04_thermodynamics/
├── 05_kinetics/
├── 06_catalysis/
└── 07_real_system/
```

Each project directory should contain the code, a small `README.md` with the prediction and result, and tests whenever there is a deterministic quantity to test.

## References / documentation

Use these as documentation and theory support, not as a prerequisite reading queue.

- George Hotz, [From the Transistor to the Web Browser](https://github.com/geohot/fromthetransistor) -- structural inspiration for this course.
- [MIT 5.61 Physical Chemistry](https://ocw.mit.edu/courses/5-61-physical-chemistry-fall-2017/) -- quantum mechanics and molecular electronic structure.
- [MIT 5.60 Thermodynamics & Kinetics](https://ocw.mit.edu/courses/5-60-thermodynamics-kinetics-spring-2008/) -- thermodynamics and kinetics foundations.
- [MIT 5.62 Physical Chemistry II](https://ocw.mit.edu/courses/5-62-physical-chemistry-ii-spring-2008/) -- statistical mechanics, molecular partition functions, equilibrium, and transition-state theory.
- [PySCF](https://pyscf.org/) -- molecular and periodic electronic-structure reference implementation.
- [ASE](https://ase-lib.org/) -- structures, calculators, optimization, MD, vibrations, NEB, and thermochemistry tooling.
- [Cantera](https://cantera.org/) -- reference kinetics / reaction-network implementation.
- Sholl & Steckel, *Density Functional Theory: A Practical Introduction* -- practical DFT reasoning.
- Nørskov et al., *Fundamental Concepts in Heterogeneous Catalysis* -- surface thermodynamics, kinetics, and catalytic descriptors.

The intended learning loop is always:

```text
predict
  ↓
build the smallest model
  ↓
calculate
  ↓
test numerically
  ↓
test physically
  ↓
explain the discrepancy
  ↓
extract a reusable rule
  ↓
apply it to a harder system
```

The final product is not a collection of scripts. It is calibrated judgment.