# Installation and dependency tiers

Use a fresh Python 3.10+ environment. The reference runs use Python 3.11.13. `pip install -e '.[test]'` provides NumPy, SciPy, ASE and pytest. `pip install -e '.[quantum]'` adds PySCF for AO integrals, molecular reference methods, gradients and Hessians. Matplotlib comes with ASE and is used only to render figures.

`requirements-lock.txt` captures the actual package versions for the generated outputs. To reproduce them, first satisfy the GPAW system dependencies, install the lock file, then install this repository with `pip install -e . --no-deps`. The core CI intentionally uses compatible dependency ranges rather than installing a periodic DFT compiler stack.

## GPAW

GPAW requires a working C compiler, BLAS and LibXC, as well as PAW setup data. Follow the [official installation documentation](https://gpaw.readthedocs.io/install.html). The reference calculations use GPAW 25.7.0 and the `gpaw-data` package; the newer default release encountered compiler/library issues on this cluster.

If system libraries are in nonstandard locations, make a GPAW build configuration, for example:

```python
# gpaw-config.py -- substitute paths to your own matching headers and shared libraries
compiler = 'gcc'
mpi = False
libraries = ['xc', 'blas']
include_dirs = ['/path/to/libxc/include']
library_dirs = ['/path/to/libxc/lib', '/path/to/blas/lib']
runtime_library_dirs = library_dirs
```

Then install on a compute node:

```bash
GPAW_CONFIG=/absolute/path/gpaw-config.py \
  python -m pip install 'gpaw==25.7.0' gpaw-data
```

Headers and libraries must have matching LibXC versions. Static libraries must be compiled with position-independent code. On the reference cluster, the matching shared LibXC and headers shipped with PySCF were available and used; BLAS was supplied by the cluster. These machine-specific paths are deliberately not hard-coded into project code.

The scheduler script uses a serial GPAW build with four CPU threads. For an MPI-enabled installation, adapt the job launcher and resources according to the site's GPAW build. Network downloads and Python environment setup can occur on the login node; expensive builds, computations and complete test runs should use Slurm on this cluster.

## Failure behavior

Missing optional libraries raise an import error. An unconverged SCF, geometry, NEB or WHAM loop raises an error rather than writing a success result. An insufficient convergence sweep is different: it writes measured results with a false tolerance flag so the numerical failure remains inspectable. No backend automatically substitutes EMT for DFT.

## Units

- General energies: eV; geometry: angstrom; temperature: K; gas input pressure: bar.
- The grid Schrodinger and LCAO projects use atomic units (Hartree, bohr).
- RHF integrals, energies and iteration history use Hartree.
- Harmonic and Lennard-Jones dynamics use declared reduced units.
- The scaled Muller–Brown surface uses model coordinates and teaching eV energies; it is not an atomistic force field.
- Molecular vibrational frequencies are cm^-1; RRHO conversion to eV precedes thermochemistry.

## Restarting the real-system sweep

Each completed adsorption task is stored in a `completed.json` checkpoint alongside its files. A checkpoint is reused only when its input, surface implementation hash and relevant library versions match. A failed or interrupted task has no completed checkpoint. Preserve the output directory and rerun the normal CLI to continue the sweep.

Independent sweep points can also be submitted as a Slurm array. The included real-system input has eight tasks (baseline plus seven variants):

```bash
sbatch --array=0-7 scripts/slurm.sh scripts/slab_task.py \
  --input 07_real_system/02_real_dft/input/example.json --output runs/real_dft
# After the array has completed, assemble and validate the aggregate:
sbatch scripts/slurm.sh 07_real_system/02_real_dft/run.py --output runs/real_dft
```

Adjust the array range if you change the sweep. Use a dependency on the array job when submitting the assembly automatically. The aggregator recalculates any missing or incompatible checkpoint, so it cannot silently turn an incomplete array into a complete result.

GPAW result convention: the project energy differences use ASE's default extrapolated electronic energy consistently for every reference. A force-consistent electronic free energy may appear in optimizer logs. Record smearing separately from the gas/surface thermodynamic temperature; do not substitute an electronic entropy correction for RRHO or configurational thermochemistry.

Restart checkpoints also fingerprint the actual Cu and H PBE PAW dataset contents selected by GPAW. Replacing a dataset at the same path invalidates the cache even if the package version is unchanged. This prevents a restart from silently mixing different electronic-structure models.
