from faasmtools.build import CMAKE_TOOLCHAIN_FILE, get_faasm_build_env_dict
from invoke import task
from os import environ, makedirs
from os.path import exists, join
from shutil import copy, rmtree
from subprocess import run
from tasks.env import EXAMPLES_DIR


@task(default=True)
def build(ctx, clean=False, native=False):
    """
    Compile TLess-JWT library (in Rust) and C++ bindings into a WASM library
    """
    jwt_dir = join(EXAMPLES_DIR, "tless-jwt", "jwt-verify")

    if clean:
        rmtree(join(jwt_dir, "target"))

    # First, cross-compile the rust library to WASM
    cargo_cmd = "cargo build --release"
    if not native:
        cargo_cmd += " --target=wasm32-wasip1"
    run(cargo_cmd, shell=True, check=True, cwd=jwt_dir)

    # Install it
    lib_dir = "/usr/local/lib/tless-jwt"
    header_dir = "/usr/include/tless-jwt"
    src_lib = join(
        jwt_dir, "target", "wasm32-wasip1" if not native else "", "release", "libtless_jwt.a"
    )
    if native:
        if not exists(lib_dir):
            if in_docker():
                makedirs(lib_dir)
            else:
                run(f"sudo mkdir -p {lib_dir}", shell=True, check=True)
        if not exists(header_dir):
            if in_docker():
                makedirs(header_dir)
            else:
                run(f"sudo mkdir -p {header_dir}", shell=True, check=True)
        dst_lib = join(lib_dir, "libtless_jwt.a")
    else:
        build_env = get_faasm_build_env_dict()
        dst_lib = join(build_env["FAASM_WASM_LIB_INSTALL_DIR"], "libtless-jwt.a")
    if in_docker():
        copy(src_lib, dst_lib)
    else:
        run(f"sudo cp {src_lib} {dst_lib}", shell=True, check=True)

    # Build the CPP bindings library, and cross-compile it to WASM
    tles_jwt_cpp_dir = join(jwt_dir, "cpp-bindings")
    build_dir = join(tles_jwt_cpp_dir, "build-native" if native else "build-wasm")

    if clean and exists(build_dir):
        rmtree(build_dir)
    if not exists(build_dir):
        makedirs(build_dir)

    cmake_cmd = [
        "cmake",
        "-GNinja",
        "-DCMAKE_BUILD_TYPE=Release",
        "-DCMAKE_TOOLCHAIN_FILE={}".format(CMAKE_TOOLCHAIN_FILE) if not native else "",
        tles_jwt_cpp_dir,
    ]
    cmake_cmd = " ".join(cmake_cmd)
    print(cmake_cmd)

    work_env = environ.copy()
    if not native:
        work_env.update(get_faasm_build_env_dict())
    run(cmake_cmd, shell=True, check=True, cwd=build_dir, env=work_env)
    run("ninja", shell=True, check=True, cwd=build_dir)

    # Install the library in the WASM sysroot
    src_lib = join(build_dir, "libtless-jwt-cpp.a")
    if not native:
        dst_lib = join(
            build_env["FAASM_WASM_LIB_INSTALL_DIR"], "libtless-jwt-cpp.a"
        )
    else:
        dst_lib = join(lib_dir, "libtless-jwt-cpp.a")
    if in_docker():
        copy(src_lib, dst_lib)
    else:
        run(f"sudo cp {src_lib} {dst_lib}", shell=True, check=True)

    # Install the header too
    src_header = join(tles_jwt_cpp_dir, "tless_jwt.h")
    if not native
        dst_header = join(
            build_env["FAASM_WASM_HEADER_INSTALL_DIR"], "tless_jwt.h"
        )
    else:
        dst_header = join(header_dir, "tless_jwt.h")
    if in_docker():
        copy(src_header, dst_header)
    else:
        run(f"sudo cp {src_header} {dst_header}", shell=True, check=True)
