from faasmtools.build import CMAKE_TOOLCHAIN_FILE, get_faasm_build_env_dict
from faasmtools.compile_util import wasm_copy_upload
from faasmtools.env import LLVM_NATIVE_VERSION
from tasks.env import DEV_FAASM_LOCAL, EXAMPLES_DIR, in_docker
from tasks.util import run_docker_build_cmd
from invoke import task
from os import environ, makedirs
from os.path import exists, join
from shutil import rmtree
from subprocess import run


@task(default=True)
def build(
    ctx, clean=False, native=False, migration=False, migration_net=False
):
    """
    Build the LAMMPS molecule dynamics simulator.

    Note that LAMMPS is a self-contained binary, and different workloads are
    executed by passing different command line arguments. As a consequence,
    we cross-compile it and copy the binary (lmp) to lammps/main/function.wasm
    """
    if migration:
        lammps_dir = join(EXAMPLES_DIR, "lammps-migration")
    if migration_net:
        lammps_dir = join(EXAMPLES_DIR, "lammps-migration-net")
    else:
        lammps_dir = join(EXAMPLES_DIR, "lammps")
    cmake_dir = join(lammps_dir, "cmake")
    if native:
        build_dir = join(lammps_dir, "build", "native")
    else:
        build_dir = join(lammps_dir, "build", "wasm")

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
        llvm_major = LLVM_NATIVE_VERSION.split(".")[0]
        cmake_cmd += [
            "-DCMAKE_C_COMPILER=/usr/bin/clang-{}".format(llvm_major),
            "-DCMAKE_CXX_COMPILER=/usr/bin/clang++-{}".format(llvm_major),
        ]
    else:
        cmake_cmd += [
            "-DLAMMPS_FAASM=ON",
            "-DCMAKE_TOOLCHAIN_FILE={}".format(CMAKE_TOOLCHAIN_FILE),
        ]
    if in_docker():
        cmake_cmd += [cmake_dir]
        cmake_cmd = " ".join(cmake_cmd)

        work_env = environ.copy()
        work_env.update(get_faasm_build_env_dict())

        run(cmake_cmd, shell=True, check=True, cwd=build_dir, env=work_env)
        run("ninja", shell=True, check=True, cwd=build_dir)

    else:
        in_docker_cmake_dir = cmake_dir
        in_docker_cmake_dir = cmake_dir.removeprefix(EXAMPLES_DIR)
        in_docker_cmake_dir = "/code/examples/examples" + in_docker_cmake_dir
        in_docker_build_dir = build_dir
        in_docker_build_dir = build_dir.removeprefix(EXAMPLES_DIR)
        in_docker_build_dir = "/code/examples/examples" + in_docker_build_dir

        cmake_cmd += [in_docker_cmake_dir]
        cmake_cmd = " ".join(cmake_cmd)

        run_docker_build_cmd(
            [cmake_cmd, "ninja"],
            cwd=in_docker_build_dir,
            env=get_faasm_build_env_dict(),
        )

    if not native:
        # Copy the binary to lammps/main/function.wasm`
        if migration:
            lammps_func_name = "migration"
        elif migration_net:
            lammps_func_name = "migration-net"
        else:
            lammps_func_name = "main"
        lammps_func = join(build_dir, "lmp")

        if in_docker():
            wasm_copy_upload("lammps", lammps_func_name, lammps_func)
        else:
            dest_folder = join(
                DEV_FAASM_LOCAL, "wasm", "lammps", lammps_func_name
            )

            makedirs(dest_folder, exist_ok=True)
            dest_file = join(dest_folder, "function.wasm")
            run(
                "sudo cp {} {}".format(lammps_func, dest_file),
                shell=True,
                check=True,
            )
