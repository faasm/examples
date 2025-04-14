from faasmtools.build import get_faasm_build_env_dict
from faasmtools.compile_util import wasm_copy_upload
from invoke import task
from os.path import join
from subprocess import run
from tasks.env import EXAMPLES_DIR


@task(default=True)
def grass(ctx, clean=False, noconf=False, debug=False):
    """
    Compile and install ImageMagick
    """
    grass_dir = join(EXAMPLES_DIR, "grass")

    if clean:
        run(
            "make clean distclean", shell=True, cwd=grass_dir, check=True
        )

    build_env = get_faasm_build_env_dict()
    build_env["GIT"] = "no"

    configure_cmd = [
        "GIT=no",
        "./configure",
        "CC={}".format(build_env["FAASM_WASM_CC"]),
        "CXX={}".format(build_env["FAASM_WASM_CXX"]),
        "CFLAGS='--target=wasm32-wasi {}'".format(build_env["FAASM_WASM_CFLAGS"]),
        "LD={}".format(build_env["FAASM_WASM_CC"]),
        "LDXX={}".format(build_env["FAASM_WASM_CXX"]),
        "LDFLAGS='{}'".format(
            build_env["FAASM_WASM_STATIC_LINKER_FLAGS"]
        ),
        "AR={}".format(build_env["FAASM_WASM_AR"]),
        "RANLIB={}".format(build_env["FAASM_WASM_RANLIB"]),
        "NM={}".format(build_env["FAASM_WASM_NM"]),
        # "PKG_CONFIG_PATH={}".format(join(EXAMPLES_DIR, "libpng")),
        "GIT=no",
        "--prefix={}".format(build_env["FAASM_WASM_SYSROOT"]),
        "--host={}".format(build_env["FAASM_WASM_TRIPLE"]),
        "--disable-openmp",
        "--disable-w11",
        "--disable-shared",
        "--without-tiff",
        "--without-zstd",
        "--enable-cross-compile",
        #         "--with-png=yes",
        #         "--enable-delegate-build",
        #         "--without-bzlib",
        #         "--without-dps",
        #         "--without-djvu",
        #         "--without-fftw",
        #         "--without-flif",
        #         "--without-fpx",
        #         "--without-fontconfig",
        #         "--without-freetype",
        #         "--without-gslib",
        #         "--without-gnu-ld",
        #         "--without-gvc",
        #         "--without-heic",
        #         "--without-jbig",
        #         "--without-lcms",
        #         "--without-lqr",
        #         "--without-magick-plus-plus",
        #         "--without-openexr",
        #         "--without-openjp2",
        #         "--without-pango",
        #         "--without-perl",
        #         "--without-raqm",
        #         "--without-raw",
        #         "--without-rsvg",
        #         "--without-threads",
        #         "--without-webp",
        #         "--without-wmf",
        #         "--without-x",
        #         "--without-xml",
    ]

    configure_cmd = " ".join(configure_cmd)
    if not noconf:
        run(configure_cmd, shell=True, cwd=grass_dir, check=True, env=build_env)

"""
    run(
        "make {} -j".format("V=1" if debug else ""),
        shell=True,
        cwd=grass_dir,
        check=True,
    )

    # Instead of installing ImageMagick, we copy the self-contained binary
    # (magick) to /usr/local/faasm/wasm/imagemagick/main/function.wasm
    wasm_copy_upload(
        "imagemagick", "main", join(grass_dir, "utilities", "magick")
    )
"""
