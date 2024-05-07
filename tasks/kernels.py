from faasmtools.env import LLVM_NATIVE_VERSION
from faasmtools.build import get_faasm_build_env_dict
from faasmtools.compile_util import wasm_copy_upload
from invoke import task
from os import environ, makedirs
from os.path import join
from shutil import rmtree
from subprocess import run
from tasks.env import EXAMPLES_DIR


def build_mpi_kernels(kernels_dir, native):
    work_env = environ.copy()
    if not native:
        work_env.update(get_faasm_build_env_dict())
        work_env["FAASM_WASM"] = "on"
    else:
        work_env.update(
            {
                "LD_LIBRARY_PATH": "/usr/local/lib",
                "LLVM_MAJOR_VERSION": LLVM_NATIVE_VERSION.split(".")[0],
                "FAASM_WASM": "off",
            }
        )

    # Build the MPI kernels
    work_env["FAASM_KERNEL_TYPE"] = "mpi"
    mpi_kernel_targets = [
        ("MPI1/AMR", "amr"),
        ("MPI1/Branch", "branch"),
        ("MPI1/DGEMM", "dgemm"),
        ("MPI1/Nstream", "nstream"),
        ("MPI1/PIC-static", "pic"),
        ("MPI1/Random", "random"),
        ("MPI1/Reduce", "reduce"),
        ("MPI1/Sparse", "sparse"),
        ("MPI1/Stencil", "stencil"),
        ("MPI1/Synch_global", "global"),
        ("MPI1/Synch_p2p", "p2p"),
        ("MPI1/Transpose", "transpose"),
    ]
    for subdir, make_target in mpi_kernel_targets:
        make_cmd = "make {}".format(make_target)
        make_dir = join(kernels_dir, subdir)
        run(make_cmd, shell=True, check=True, cwd=make_dir, env=work_env)
        if not native:
            wasm_copy_upload(
                "kernels-mpi",
                make_target,
                join(
                    kernels_dir,
                    "build",
                    "wasm",
                    "mpi_{}.wasm".format(make_target),
                ),
            )


def build_omp_kernels(kernels_dir, native):
    work_env = environ.copy()
    if not native:
        work_env.update(get_faasm_build_env_dict(is_threads=True))
        work_env["FAASM_WASM"] = "on"
    else:
        work_env.update(
            {
                "LD_LIBRARY_PATH": "/usr/local/lib",
                "LLVM_MAJOR_VERSION": LLVM_NATIVE_VERSION.split(".")[0],
                "FAASM_WASM": "off",
            }
        )

    # Build the OMP kernels
    work_env["FAASM_KERNEL_TYPE"] = "omp"
    omp_kernel_targets = [
        ("OPENMP/Synch_global", "global"),
        ("OPENMP/Synch_p2p", "p2p"),
        ("OPENMP/Sparse", "sparse"),
        ("OPENMP/DGEMM", "dgemm"),
        ("OPENMP/Nstream", "nstream"),
        ("OPENMP/Reduce", "reduce"),
        # TODO: build fails for these kernels
        # ("OPENMP/Stencil", "stencil"),
        # ("OPENMP/Random", "random"),
        # ("OPENMP/Transpose", "transpose"),
    ]
    for subdir, make_target in omp_kernel_targets:
        make_cmd = "make {}".format(make_target)
        make_dir = join(kernels_dir, subdir)
        run(make_cmd, shell=True, check=True, cwd=make_dir, env=work_env)
        if not native:
            wasm_copy_upload(
                "kernels-omp",
                make_target,
                join(
                    kernels_dir,
                    "build",
                    "wasm",
                    "omp_{}.wasm".format(make_target),
                ),
            )


@task(default=True)
def build(ctx, clean=False, native=False, elastic=False):
    """
    Build the different kernels functions for OpenMP and MPI

    Note that LAMMPS is a self-contained binary, and different workloads are
    executed by passing different command line arguments. As a consequence,
    we cross-compile it and copy the binary (lmp) to lammps/main/function.wasm
    """
    if elastic:
        kernels_dir = join(EXAMPLES_DIR, "Kernels-elastic")
    else:
        kernels_dir = join(EXAMPLES_DIR, "Kernels")

    if native:
        build_dir = join(kernels_dir, "build", "native")
    else:
        build_dir = join(kernels_dir, "build", "wasm")

    if clean:
        run("make clean", shell=True, check=True, cwd=kernels_dir)
        rmtree(build_dir)

    makedirs(join(kernels_dir, "build"), exist_ok=True)
    makedirs(build_dir, exist_ok=True)

    # When building the elastic kernels we only need to build the OpenMP ones
    if elastic:
        build_omp_kernels(kernels_dir, native)
    else:
        build_mpi_kernels(kernels_dir, native)
        # Clean MPI wasm files
        run("make clean", shell=True, check=True, cwd=kernels_dir)
        build_omp_kernels(kernels_dir, native)
