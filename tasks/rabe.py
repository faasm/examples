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
    Compile rabe library (in Rust) and C++ bindings into a WASM library
    """
    rabe_dir = join(EXAMPLES_DIR, "rabe")

    if clean:
        rmtree(join(rabe_dir, "target"))

    # First, cross-compile the rust library to WASM
    cargo_cmd = "cargo build --release"
    if not native:
        cargo_cmd += "--target=wasm32-wasip1"

    run(cargo_cmd, shell=True, check=True, cwd=rabe_dir)

    lib_dir = "/usr/local/lib/rabe"
    header_dir = "/usr/include/rabe"
    if not native:
        build_env = get_faasm_build_env_dict()
        lib_dir = build_env["FAASM_WASM_LIB_INSTALL_DIR"]
        header_dir = build_env["FAASM_WASM_HEADER_INSTALL_DIR"]
    else:
        if not exists(lib_dir):
            makedirs(lib_dir)
        if not exists(header_dir):
            makedirs(header_dir)

    if not native:
        src_lib = join(rabe_dir, "target", "wasm32-wasip1", "release", "librabe.a")
    else:
        src_lib = join(rabe_dir, "target", "release", "librabe.a")

    dst_lib = join(lib_dir, "librabe.a")
    copy(src_lib, dst_lib)

    # Build the CPP bindings library, and cross-compile it to WASM
    rabe_cpp_dir = join(rabe_dir, "cpp-bindings")

    if native:
        build_dir = join(rabe_cpp_dir, "build-native")
    else:
        build_dir = join(rabe_cpp_dir, "build-wasm")

    if clean and exists(build_dir):
        rmtree(build_dir)
    if not exists(build_dir):
        makedirs(build_dir)

    cmake_cmd = [
        "cmake",
        "-GNinja",
        "-DCMAKE_BUILD_TYPE=Release",
        "-DCMAKE_TOOLCHAIN_FILE={}".format(CMAKE_TOOLCHAIN_FILE) if not native else "",
        rabe_cpp_dir,
    ]
    cmake_cmd = " ".join(cmake_cmd)
    print(cmake_cmd)

    work_env = environ.copy()
    work_env.update(get_faasm_build_env_dict())
    run(cmake_cmd, shell=True, check=True, cwd=build_dir, env=work_env)
    run("ninja", shell=True, check=True, cwd=build_dir)

    # Install the CPP bindings library
    src_lib = join(build_dir, "librabe-cpp.a")
    dst_lib = join(lib_dir, "librabe-cpp.a")
    copy(src_lib, dst_lib)

    # Install the headers
    src_header = join(rabe_cpp_dir, "rabe_bindings.hpp")
    dst_header = join(header_dir, "tless_abe.h")
    copy(src_header, dst_header)
    src_header = join(rabe_cpp_dir, "tless_aes.h")
    dst_header = join(header_dir, "tless_aes.h")
    copy(src_header, dst_header)
