from faasmtools.build import get_faasm_build_env_dict
from invoke import task
from os.path import join
from subprocess import run
from tasks.env import EXAMPLES_DIR


@task(default=True)
def ffmpeg(ctx, clean=False):
    """
    Compile and install FFmpeg
    """
    ffmpeg_dir = join(EXAMPLES_DIR, "FFmpeg")

    if clean:
        run("make clean", shell=True, cwd=ffmpeg_dir, check=True)

    build_env = get_faasm_build_env_dict()

    # List of flags inspired from the github project:
    # https://github.com/ffmpegwasm/ffmpeg.wasm-core
    configure_cmd = [
        "./configure",
        "--prefix={}".format(build_env["FAASM_WASM_SYSROOT"]),
        "--libdir={}".format(build_env["FAASM_WASM_HEADER_INSTALL_DIR"]),
        "--target-os=none",
        "--arch=x86_32",
        "--enable-cross-compile",
        "--disable-x86asm",
        "--disable-inline-asm",
        "--disable-network",
        "--disable-stripping",
        "--disable-programs",
        "--disable-doc",
        "--disable-zlib",
        "--extra-cflags='{}'".format(build_env["FAASM_WASM_CFLAGS"]),
        "--extra-cxxflags='{}'".format(build_env["FAASM_WASM_CXXFLAGS"]),
        "--extra-ldflags='{}'".format(
            build_env["FAASM_WASM_STATIC_LINKER_FLAGS"]
        ),
        "--nm={}".format(build_env["FAASM_WASM_NM"]),
        "--ar={}".format(build_env["FAASM_WASM_AR"]),
        "--ranlib={}".format(build_env["FAASM_WASM_RANLIB"]),
        "--cc={}".format(build_env["FAASM_WASM_CC"]),
        "--cxx={}".format(build_env["FAASM_WASM_CXX"]),
        "--objcc={}".format(build_env["FAASM_WASM_CC"]),
        "--dep-cc={}".format(build_env["FAASM_WASM_CC"]),
    ]

    configure_cmd = " ".join(configure_cmd)
    run(configure_cmd, shell=True, cwd=ffmpeg_dir, check=True)

    run("make -j", shell=True, cwd=ffmpeg_dir, check=True)

    run("make install", shell=True, cwd=ffmpeg_dir, check=True)
