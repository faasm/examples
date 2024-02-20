from faasmtools.build import CMAKE_TOOLCHAIN_FILE, get_faasm_build_env_dict
from faasmtools.compile_util import wasm_copy_upload
from faasmtools.env import LLVM_VERSION
from tasks.env import EXAMPLES_DIR
from invoke import task
from os import environ, listdir, makedirs
from os.path import exists, join
from shutil import rmtree
from subprocess import run


@task(default=True)
def build(ctx, clean=False, native=False):
    """
    Build the PolyBench/C benchmark
    """
    polybench_dir = join(EXAMPLES_DIR, "polybench")
    if native:
        build_dir = join(polybench_dir, "build", "native")
    else:
        build_dir = join(polybench_dir, "build", "wasm")

    if clean and exists(build_dir):
        rmtree(build_dir)

    if not exists(build_dir):
        makedirs(build_dir)

    cmake_cmd = [
        "cmake",
        "-GNinja",
        "-DCMAKE_BUILD_TYPE=Release",
    ]

    if native:
        llvm_major = LLVM_VERSION.split(".")[0]
        cmake_cmd += [
            "-DCMAKE_C_COMPILER=/usr/bin/clang-{}".format(llvm_major),
            "-DCMAKE_CXX_COMPILER=/usr/bin/clang++-{}".format(llvm_major),
        ]
    else:
        cmake_cmd += [
            "-DFAASM_BUILD_TYPE=wasm",
            "-DCMAKE_TOOLCHAIN_FILE={}".format(CMAKE_TOOLCHAIN_FILE),
        ]
    cmake_cmd += [polybench_dir]
    cmake_cmd = " ".join(cmake_cmd)

    work_env = environ.copy()
    work_env.update(get_faasm_build_env_dict())

    run(cmake_cmd, shell=True, check=True, cwd=build_dir, env=work_env)
    run(
        "cmake --build . --target polybench_all",
        shell=True,
        check=True,
        cwd=build_dir,
    )

    if not native:
        # Copy all the functions to /usr/local/faasm/wasm/polybench/*
        for poly_func in [
            f for f in listdir(build_dir) if f.startswith("poly_")
        ]:
            wasm_copy_upload(
                "polybench", poly_func, join(build_dir, poly_func)
            )
