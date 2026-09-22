# The Molecular Hamiltonian

## 1. Full electron-nuclear Hamiltonian

For a non-relativistic molecular system,

$$
\hat H =
-\sum_A \frac{\hbar^2}{2M_A}\nabla_A^2
-\sum_i \frac{\hbar^2}{2m_e}\nabla_i^2
-\sum_{i,A}\frac{Z_A e^2}{4\pi\epsilon_0 r_{iA}}
+\sum_{i<j}\frac{e^2}{4\pi\epsilon_0 r_{ij}}
+\sum_{A<B}\frac{Z_A Z_B e^2}{4\pi\epsilon_0 R_{AB}}
$$

Identify the terms:

1. Nuclear kinetic energy
2. Electronic kinetic energy
3. Electron-nuclear attraction
4. Electron-electron repulsion
5. Nuclear-nuclear repulsion

## 2. Born-Oppenheimer approximation

Because

$$
M_A \gg m_e,
$$

electrons respond much faster than nuclei.

We therefore approximately separate

$$
\Psi(\mathbf r,\mathbf R)
\approx
\psi_e(\mathbf r;\mathbf R)\chi(\mathbf R).
$$

For fixed nuclear positions $\mathbf R$,

$$
\hat H_e(\mathbf R)\psi_e
=
E_e(\mathbf R)\psi_e.
$$

The electronic energy as a function of nuclear geometry defines the potential-energy surface.

## 3. What is the potential-energy surface?

$$
E_{\mathrm{PES}}(\mathbf R)
=
E_e(\mathbf R)
+
V_{NN}(\mathbf R)
$$

Geometry optimization searches for a local minimum:

$$
\nabla_{\mathbf R}E(\mathbf R)=0.
$$

A first-order transition state has one unstable direction:

$$
\lambda_1 < 0,
\qquad
\lambda_{i>1}>0.
$$

## 4. Where the approximations enter

Exact many-body Schrödinger equation
↓
Born-Oppenheimer approximation
↓
Electronic-structure approximation
↓
HF / DFT / correlated wavefunction methods
↓
Potential-energy surface
↓
Statistical mechanics
↓
Free energy
↓
TST / dynamics
↓
Microkinetics
↓
Experimental observable

## 5. What each method actually gives me

| Method | Main output | What it does NOT automatically give |
|---|---|---|
| DFT | Electronic energy, forces | Finite-T free energy |
| Geometry optimization | Local minimum | Global minimum |
| NEB | Approximate MEP/barrier | Finite-T rate |
| MD | Trajectory | Exhaustive sampling |
| OPES / metadynamics | Biased free-energy landscape | Unique mechanism |
| TST | Rate estimate | Exact dynamics |
| Microkinetics | TOF/coverage from a model | Proof the mechanism is complete |

## 6. Questions I should be able to answer

- Why can nuclei be treated approximately as fixed during an electronic-structure calculation?
- What exactly is being minimized in a geometry optimization?
- Is a DFT total energy a Gibbs free energy?
- Why can two perfectly converged DFT calculations disagree?
- Why does a NEB barrier not directly equal an experimental activation energy?
- Where do entropy and temperature first enter the stack?
