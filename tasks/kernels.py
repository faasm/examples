from faasmtools.build import FAASM_BUILD_ENV_DICT
from faasmtools.compile_util import wasm_copy_upload
from invoke import task
from os import environ, makedirs
from os.path import join
from shutil import rmtree
from subprocess import run
from tasks.env import EXAMPLES_DIR


@task(default=True)
def build(ctx, clean=False, native=False):
    """
    Build the different kernels functions for OpenMP and MPI

    Note that LAMMPS is a self-contained binary, and different workloads are
    executed by passing different command line arguments. As a consequence,
    we cross-compile it and copy the binary (lmp) to lammps/main/function.wasm
    """
    kernels_dir = join(EXAMPLES_DIR, "Kernels")

    if clean:
        run("make clean", shell=True, check=True, cwd=kernels_dir)
        if native:
            rmtree(join(kernels_dir, "build", "native"))
        else:
            rmtree(join(kernels_dir, "build", "wasm"))

    if native:
        makedirs(join(kernels_dir, "build", "native"), exist_ok=True)
    else:
        makedirs(join(kernels_dir, "build", "wasm"), exist_ok=True)

    work_env = environ.copy()
    if not native:
        work_env.update(FAASM_BUILD_ENV_DICT)
        work_env["FAASM_WASM"] = "on"
    else:
        work_env.update(
            {
                "LD_LIBRARY_PATH": "/usr/local/lib",
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

    # Clean MPI wasm files
    run("make clean", shell=True, check=True, cwd=kernels_dir)

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
