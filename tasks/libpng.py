from faasmtools.build import get_faasm_build_env_dict
from invoke import task
from os import listdir, makedirs
from os.path import exists, join
from subprocess import run
from tasks.env import EXAMPLES_DIR


@task(default=True)
def libpng(ctx, clean=False):
    """
    Compile and install libpng
    """
    libpng_dir = join(EXAMPLES_DIR, "libpng")

    if clean:
        run("make clean", shell=True, cwd=libpng_dir, check=True)

    build_env = get_faasm_build_env_dict()

    # 30/01/2022 - SIMD not working with ImageMagick, so we must also not use
    # SIMD when building libpng
    wasm_cflags_nosimd = build_env["FAASM_WASM_CFLAGS"]
    wasm_cflags_nosimd = wasm_cflags_nosimd.replace("-msimd128", "")

    # Instead of running a complicated configure, we use a simplified makefile
    # under `faasm/libpng/scripts/makefile.wasm` to build _only_ libpng
    make_cmd = [
        "WASM_CC={}".format(build_env["FAASM_WASM_CC"]),
        "WASM_AR={}".format(build_env["FAASM_WASM_AR"]),
        "WASM_RANLIB={}".format(build_env["FAASM_WASM_RANLIB"]),
        "WASM_CFLAGS='{}'".format(" ".join(wasm_cflags_nosimd)),
        "WASM_LDFLAGS='{}'".format(
            build_env["FAASM_WASM_STATIC_LINKER_FLAGS"]
        ),
        "WASM_SYSROOT={}".format(build_env["FAASM_WASM_SYSROOT"]),
        "make -j",
    ]
    make_cmd = " ".join(make_cmd)
    run(make_cmd, shell=True, cwd=libpng_dir, check=True)

    # Install static library
    cp_cmd = "cp {}/libpng.a {}/libpng16.a".format(
        libpng_dir, build_env["FAASM_WASM_LIB_INSTALL_DIR"]
    )
    run(cp_cmd, shell=True, check=True)
    print(cp_cmd)

    # Install headers
    libpng_header_install_dir = join(
        build_env["FAASM_WASM_HEADER_INSTALL_DIR"], "libpng16"
    )
    if not exists(libpng_header_install_dir):
        makedirs(libpng_header_install_dir)
    header_files = [
        join(libpng_dir, hf) for hf in listdir(libpng_dir) if hf.endswith(".h")
    ]
    cp_cmd = "cp {} {}/".format(
        " ".join(header_files), libpng_header_install_dir
    )
    print(cp_cmd)
    run(cp_cmd, shell=True, check=True)
