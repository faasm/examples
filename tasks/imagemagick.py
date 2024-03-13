from faasmtools.build import get_faasm_build_env_dict
from faasmtools.compile_util import wasm_copy_upload
from invoke import task
from os.path import join
from subprocess import run
from tasks.env import EXAMPLES_DIR


@task(default=True)
def imagemagick(ctx, clean=False, noconf=False, debug=False):
    """
    Compile and install ImageMagick
    """
    imagemagick_dir = join(EXAMPLES_DIR, "ImageMagick")

    if clean:
        run(
            "make clean distclean", shell=True, cwd=imagemagick_dir, check=True
        )

    build_env = get_faasm_build_env_dict()

    # 30/01/2022 - SIMD not working with ImageMagick. We manually remove the
    # flags
    wasm_cflags_nosimd = build_env["FAASM_WASM_CFLAGS"]
    wasm_cflags_nosimd = wasm_cflags_nosimd.replace("-msimd128", "")
    wasm_cflags_nosimd += " -I{}".format(
        join(build_env["FAASM_WASM_HEADER_INSTALL_DIR"], "libpng16")
    )

    # List of flags inspired from the github project:
    # https://github.com/KnicKnic/WASM-ImageMagick
    # For all the configure options, see:
    # https://github.com/ImageMagick/ImageMagick/blob/main/Install-unix.txt
    configure_cmd = [
        "./configure",
        "CC={}".format(build_env["FAASM_WASM_CC"]),
        "CXX={}".format(build_env["FAASM_WASM_CXX"]),
        "CFLAGS='--target=wasm32-wasi {}'".format(wasm_cflags_nosimd),
        "LD={}".format(build_env["FAASM_WASM_CC"]),
        "LDXX={}".format(build_env["FAASM_WASM_CXX"]),
        "LDFLAGS='{}'".format(
            build_env["FAASM_WASM_STATIC_LINKER_FLAGS"]
        ),  # wasm_ldflags_nosimd),
        "AR={}".format(build_env["FAASM_WASM_AR"]),
        "RANLIB={}".format(build_env["FAASM_WASM_RANLIB"]),
        "NM={}".format(build_env["FAASM_WASM_NM"]),
        "PKG_CONFIG_PATH={}".format(join(EXAMPLES_DIR, "libpng")),
        "--prefix={}".format(build_env["FAASM_WASM_SYSROOT"]),
        "--disable-largefile",
        "--disable-modules",
        "--disable-openmp",
        "--disable-shared",
        "--host={}".format(build_env["FAASM_WASM_TRIPLE"]),
        "--with-png=yes",
        "--enable-delegate-build",
        "--without-bzlib",
        "--without-dps",
        "--without-djvu",
        "--without-fftw",
        "--without-flif",
        "--without-fpx",
        "--without-fontconfig",
        "--without-freetype",
        "--without-gslib",
        "--without-gnu-ld",
        "--without-gvc",
        "--without-heic",
        "--without-jbig",
        "--without-lcms",
        "--without-lqr",
        "--without-magick-plus-plus",
        "--without-openexr",
        "--without-openjp2",
        "--without-pango",
        "--without-perl",
        "--without-raqm",
        "--without-raw",
        "--without-rsvg",
        "--without-threads",
        "--without-webp",
        "--without-wmf",
        "--without-x",
        "--without-xml",
    ]

    configure_cmd = " ".join(configure_cmd)
    if not noconf:
        run(configure_cmd, shell=True, cwd=imagemagick_dir, check=True)

    run(
        "make {} -j".format("V=1" if debug else ""),
        shell=True,
        cwd=imagemagick_dir,
        check=True,
    )

    # Instead of installing ImageMagick, we copy the self-contained binary
    # (magick) to /usr/local/faasm/wasm/imagemagick/main/function.wasm
    wasm_copy_upload(
        "imagemagick", "main", join(imagemagick_dir, "utilities", "magick")
    )
