from faasmtools.build import CMAKE_TOOLCHAIN_FILE, get_faasm_build_env_dict
from invoke import task
from os import environ, makedirs
from os.path import exists, join
from shutil import copy, rmtree
from subprocess import run
from tasks.env import EXAMPLES_DIR


@task(default=True)
def build(ctx, clean=False):
    """
    Compile TLess-JWT library (in Rust) and C++ bindings into a WASM library
    """
    jwt_dir = join(EXAMPLES_DIR, "tless-jwt", "jwt-verify")

    if clean:
        rmtree(join(jwt_dir, "target"))

    # First, cross-compile the rust library to WASM
    cargo_cmd = "cargo build --release --target=wasm32-wasip1"
    run(cargo_cmd, shell=True, check=True, cwd=jwt_dir)

    # Install it in the WASM sysroot
    build_env = get_faasm_build_env_dict()
    src_lib = join(jwt_dir, "target", "wasm32-wasip1", "release", "libtless_jwt.a")
    dst_lib = join(build_env["FAASM_WASM_LIB_INSTALL_DIR"], "libtless-jwt.a")
    copy(src_lib, dst_lib)

    # Build the CPP bindings library, and cross-compile it to WASM
    rabe_cpp_dir = join(jwt_dir, "cpp-bindings")
    build_dir = join(rabe_cpp_dir, "build")

    if clean and exists(build_dir):
        rmtree(build_dir)
    if not exists(build_dir):
        makedirs(build_dir)

    cmake_cmd = [
        "cmake",
        "-GNinja",
        "-DCMAKE_BUILD_TYPE=Release",
        "-DCMAKE_TOOLCHAIN_FILE={}".format(CMAKE_TOOLCHAIN_FILE),
        rabe_cpp_dir,
    ]
    cmake_cmd = " ".join(cmake_cmd)
    print(cmake_cmd)

    work_env = environ.copy()
    work_env.update(get_faasm_build_env_dict())
    print(build_dir)
    run(cmake_cmd, shell=True, check=True, cwd=build_dir, env=work_env)
    run("ninja", shell=True, check=True, cwd=build_dir)

    # Install the library in the WASM sysroot
    src_lib = join(build_dir, "libtless-jwt-cpp.a")
    dst_lib = join(build_env["FAASM_WASM_LIB_INSTALL_DIR"], "libtless-jwt-cpp.a")
    copy(src_lib, dst_lib)

    # Install the header in the WASM sysroot too
    src_header = join(rabe_cpp_dir, "tless_jwt.h")
    dst_header = join(
        build_env["FAASM_WASM_HEADER_INSTALL_DIR"], "tless_jwt.h"
    )
    copy(src_header, dst_header)
