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
| --- | --- | --- | --- |
| [FFmpeg](https://github.com/faasm/FFmpeg) | :white_check_mark: | :white_check_mark: | :x: |
| [Kernels](https://github.com/faasm/Kernels) | :white_check_mark: | :x: | :x: |
| [LAMMPS](https://github.com/faasm/lammps) | :white_check_mark: | :white_check_mark: | :x: |
| [libpng](https://github.com/faasm/libpng) | :white_check_mark: | :white_check_mark: | :x: |
| [ImageMagick](https://github.com/faasm/ImageMagick) | :white_check_mark: | :white_check_mark: | :x: |
| [LULESH](https://github.com/faasm/LULESH) | :white_check_mark: | :x: | :x: |
| [PolyBench/C](https://github.com/faasm/polybench) | :white_check_mark: | :white_check_mark: | :x: |
| [Tensorflow](https://github.com/faasm/tensorflow) | :white_check_mark: | :white_check_mark: | :x: |

## Bumping C++, Python, or Faasm's version

This repository depends on Faasm's toolchain repos ([C++](https://github.com/faasm/cpp),
and [Python](https://github.com/faasm/python)) and the [Faasm runtime](
https://github.com/faasm/faasm). As a consequence, it is versioned with the
versions of the previous.

If you want to upgrade the Python or C++ tag, you must update the submodule
and the files that track either version. You can do:

```bash
cd cpp
git pull origin main
cd ..
inv git.bump cpp
```

Similarly, for Faasm you can just do:

```bash
inv git.bump faasm [--ver=<specific_version>]
```

Then, tag the new version and re-build the docker images:

```bash
inv git.tag
inv docker.build -c build -c run --nocache --push
```

## Adding a new application

To add a new application, you first need to cross-compile it to WebAssembly.
You can check the [`tasks/`](./tasks) folder for examples of how we do it for
existing applications. Most importantly, you will have to inidicate the right
sysroot, and pass the environment variables that we read from `faasmtools`.

Once the application is cross-compiled, you must make it run with Faasm. The
tests in GHA only test integration with the WAVM runtime in Faasm, but if you
need to pick another one for a very specific reason, it can also be tested.
