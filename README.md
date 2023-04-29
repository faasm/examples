# Example Applications for Faasm

This repository contains a list of applications and libraries that have been
cross-compiled to WebAssembly for their use with Faasm.

> WARNING: examples listed here have worked _at some point_ in time. The fact
> that they are listed here does not mean that they still run, or that they
> are supported in any way.

## Quick Start

To cross-compile any of the supported applications for its usage with Faasm,
you must first start the build client:

```bash
source ./bin/workon.sh
inv cli build
```

Inside the build client, you can list the available tasks, and cross-compile
any of the supported libraries/applications:

```bash
inv -l
inv lammps [--clean]
```

You can access the generated WASM file both from inside and outside the build
client container.

```bash
# Outside the container
ls ./dev/faasm-local/wasm

# For LAMMPS
file ./dev/faasm-local/wasm/lammps/main/function.wasm
```

This WASM file is ready to be uploaded to a Faasm cluster using the HTTP API.

## List of examples

| Project Name | WAVM | WAMR | WAMR + SGX |
| --- | --- | --- |
| [FFmpeg](https://github.com/faasm/FFmpeg) | C, C++ | Static library |
| [Kernels](https://github.com/faasm/Kernels) | C, C++ | OpenMP, MPI |
| [LAMMPS](https://github.com/faasm/lammps) | C++ | MPI |
| [libpng](https://github.com/faasm/libpng) | C | Static library |
| [ImageMagick](https://github.com/faasm/ImageMagick) | C++ | Needs libpng |
| [LULESH](https://github.com/faasm/LULESH) | C++ | OpenMP |
| [Tensorflow](https://github.com/faasm/tensorflow) | C++ | Static library |

## Bumping C++, Python, or Faasm's version

This repository depends on Faasm's toolchain repos ([C++](https://github.com/faasm/cpp),
and [Python](https://github.com/faasm/python)) and the [Faasm runtime](
https://github.com/faasm/faasm). As a consequence, it is versioned with the
versions of the previous.

If you want to upgrade the Python or C++ tag, you must update the submodule
and the GHA file. If you want to update the Faasm tag, you must update the
`FAASM_VERSION` file, and the GHA file. Then, re-build the container images
with:

```bash
inv docker.build -c build -c run --nocache --push
```

## Adding a new application

To add a new application, you first need to cross-compile it to WebAssembly.
You can check the [`tasks/`]](./tasks) folder for examples of how we do it for
existing applications. Most importantly, you will have to inidicate the right
sysroot, and pass the environment variables that we read from `faasmtools`.

Once the application is cross-compiled, you must make it run with Faasm. The
tests in GHA only test integration with the WAVM runtime in Faasm, but if you
need to pick another one for a very specific reason, it can also be tested.
