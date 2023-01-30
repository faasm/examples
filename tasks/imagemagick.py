from faasmtools.build import (
    WASM_AR,
    WASM_CC,
    WASM_CFLAGS,
    WASM_CXX,
    WASM_EXE_LDFLAGS,
    WASM_HOST,
    WASM_LD,
    WASM_NM,
    WASM_RANLIB,
    WASM_SYSROOT,
)
from faasmtools.compile_util import wasm_copy_upload
from invoke import task
from os.path import join
from subprocess import run
from tasks.env import EXAMPLES_DIR


@task(default=True)
def imagemagick(ctx, clean=False):
    """
    Compile and install ImageMagick
    """
    imagemagick_dir = join(EXAMPLES_DIR, "ImageMagick")

    if clean:
        run("make clean", shell=True, cwd=imagemagick_dir, check=True)

    # 30/01/2022 - SIMD not working with ImageMagick. We manually remove the
    # flags
    wasm_cflags_nosimd = WASM_CFLAGS
    try:
        wasm_cflags_nosimd.remove("-msimd128")
    except ValueError:
        pass
    wasm_cflags_nosimd.append(
        "-I{}".format(join(WASM_SYSROOT, "include", "libpng16"))
    )
    wasm_ldflags_nosimd = WASM_EXE_LDFLAGS
    for ldflag in WASM_EXE_LDFLAGS:
        if "simd128" in ldflag:
            try:
                wasm_ldflags_nosimd.remove(ldflag)
            except ValueError:
                pass
            wasm_ldflags_nosimd.append("-Xlinker --no-check-features")

    # List of flags inspired from the github project:
    # https://github.com/KnicKnic/WASM-ImageMagick
    # For all the configure options, see:
    # https://github.com/ImageMagick/ImageMagick/blob/main/Install-unix.txt
    configure_cmd = [
        "./configure",
        "CC={}".format(WASM_CC),
        "CXX={}".format(WASM_CXX),
        "CFLAGS='{}'".format(" ".join(wasm_cflags_nosimd)),
        "CXXFLAGS='{}'".format(" ".join(wasm_cflags_nosimd)),
        "LD={}".format(WASM_LD),
        "LDFLAGS='{}'".format(" ".join(wasm_ldflags_nosimd)),
        "CXXLDFLAGS='{}'".format(" ".join(wasm_ldflags_nosimd)),
        "AR={}".format(WASM_AR),
        "RANLIB={}".format(WASM_RANLIB),
        "NM={}".format(WASM_NM),
        "PKG_CONFIG_PATH={}".format(join(EXAMPLES_DIR, "libpng")),
        "--prefix={}".format(WASM_SYSROOT),
        "--disable-largefile",
        "--disable-modules",
        "--disable-openmp",
        "--disable-shared",
        "--host={}".format(WASM_HOST),
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
    run(configure_cmd, shell=True, cwd=imagemagick_dir, check=True)

    run("make -j", shell=True, cwd=imagemagick_dir, check=True)

    # Instead of installing ImageMagick, we copy the self-contained binary
    # (magick) to /usr/local/faasm/wasm/imagemagick/main/function.wasm
    wasm_copy_upload(
        "imagemagick", "main", join(imagemagick_dir, "utilities", "magick")
    )
