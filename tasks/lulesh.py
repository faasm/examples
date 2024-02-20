from faasmtools.build import CMAKE_TOOLCHAIN_FILE, get_faasm_build_env_dict
from faasmtools.compile_util import wasm_copy_upload
from invoke import task
from os import environ, makedirs
from os.path import exists, join
from shutil import rmtree
from subprocess import run
from tasks.env import EXAMPLES_DIR


@task(default=True)
def build(ctx, clean=False, native=False):
    """
    Build the LULESH explicit shock hydrodynamics simulator

    Note that LULESH is a self-contained binary, and different workloads are
    executed by passing different command line arguments. As a consequence,
    we cross-compile it and copy the binary (lulesh2.0) to
    lulesh/main/function.wasm
    """
    lulesh_dir = join(EXAMPLES_DIR, "LULESH")
    if native:
        build_dir = join(lulesh_dir, "build", "native")
    else:
        build_dir = join(lulesh_dir, "build", "wasm")

    if clean and exists(build_dir):
        rmtree(build_dir)

    if not exists(build_dir):
        makedirs(build_dir)

    cmake_cmd = [
        "cmake",
        "-GNinja",
        "-DCMAKE_BUILD_TYPE=Release",
        "-DWITH_MPI=FALSE",
        "{}".format("-DWITH_FAASM=TRUE" if not native else ""),
        "{}".format(
            "-DCMAKE_TOOLCHAIN_FILE={}".format(CMAKE_TOOLCHAIN_FILE)
            if not native
            else ""
        ),
        lulesh_dir,
    ]
    cmake_cmd = " ".join(cmake_cmd)

    work_env = environ.copy()
    if not native:
        work_env.update(get_faasm_build_env_dict(is_threads=True))

    run(cmake_cmd, shell=True, check=True, cwd=build_dir, env=work_env)
    run("cmake --build . --target all", shell=True, check=True, cwd=build_dir)

    if not native:
        # Copy the binary to lulesh/main/function.wasm
        wasm_copy_upload("lulesh", "main", join(build_dir, "lulesh2.0"))
