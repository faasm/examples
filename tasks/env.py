from faasmtools.build import FAASM_LOCAL_DIR
from faasmtools.docker import ACR_NAME
from faasmtools.env import get_version as get_cpp_version
from os import environ
from os.path import dirname, abspath, join
from yaml import safe_load

PROJ_ROOT = dirname(dirname(abspath(__file__)))
EXAMPLES_IN_DOCKER_ROOT = "/code/examples"
DOCKER_ROOT = join(PROJ_ROOT, "docker")
EXAMPLES_DIR = join(PROJ_ROOT, "examples")
DEV_FAASM_LOCAL = join(PROJ_ROOT, "dev", "faasm-local")
WASM_DIR = join(PROJ_ROOT, "wasm")

# Docker variables
EXAMPLES_BUILD_IMAGE_CTR = "examples-build-workon"
EXAMPLES_BUILD_IMAGE_NAME = "{}/examples-build".format(ACR_NAME)
EXAMPLES_BUILD_DOCKERFILE = join(DOCKER_ROOT, "build.dockerfile")
EXAMPLES_BASE_IMAGE_NAME = "{}/examples-base".format(ACR_NAME)
EXAMPLES_BASE_DOCKERFILE = join(DOCKER_ROOT, "base.dockerfile")

# Shared files data
EXAMPLES_DATA_BASE_DIR = join(FAASM_LOCAL_DIR, "shared")
EXAMPLES_DATA_HOST_DIR = join(PROJ_ROOT, "data")
EXAMPLES_DATA_FILES = [
    [
        join(EXAMPLES_DATA_HOST_DIR, "faasm_logo.png"),
        join(EXAMPLES_DATA_BASE_DIR, "im", "sample_image.png"),
    ],
    [
        join(EXAMPLES_DATA_HOST_DIR, "in.controller.wall"),
        join(EXAMPLES_DATA_BASE_DIR, "lammps-data", "in.controller.wall"),
    ],
    [
        join(EXAMPLES_DATA_HOST_DIR, "ffmpeg_video.mp4"),
        join(EXAMPLES_DATA_BASE_DIR, "ffmpeg", "sample_video.mp4"),
    ],
    [
        join(EXAMPLES_DATA_HOST_DIR, "sample_model.tflite"),
        join(EXAMPLES_DATA_BASE_DIR, "tflite", "sample_model.tflite"),
    ],
    [
        join(EXAMPLES_DATA_HOST_DIR, "grace_hopper.bmp"),
        join(EXAMPLES_DATA_BASE_DIR, "tflite", "grace_hopper.bmp"),
    ],
    [
        join(EXAMPLES_DATA_HOST_DIR, "bus_photo.bmp"),
        join(EXAMPLES_DATA_BASE_DIR, "opencv", "bus_photo.bmp"),
    ],
    [
        join(EXAMPLES_DATA_HOST_DIR, "tchaikovsky.bmp"),
        join(EXAMPLES_DATA_BASE_DIR, "opencv", "composers", "tchaikovsky.bmp"),
    ],
    [
        join(EXAMPLES_DATA_HOST_DIR, "wagner.bmp"),
        join(EXAMPLES_DATA_BASE_DIR, "opencv", "composers", "wagner.bmp"),
    ],
    [
        join(EXAMPLES_DATA_HOST_DIR, "beethoven.bmp"),
        join(EXAMPLES_DATA_BASE_DIR, "opencv", "composers", "beethoven.bmp"),
    ],
]


def get_submodule_version(submodule):
    """
    Get the version of a submodule as indicated in the VERSION file
    """
    ver_file = join(PROJ_ROOT, submodule, "VERSION")

    with open(ver_file, "r") as fh:
        version = fh.read()

    version = version.strip()
    return version


def get_python_version():
    """
    Get the version of the python submodule
    """
    return get_submodule_version("python")


def get_faasm_version():
    """
    Get the version of the Faasm dependency
    """
    yaml_path = join(PROJ_ROOT, ".github", "workflows", "tests.yml")
    return safe_load(open(yaml_path, "r"))["jobs"]["run-examples-faasmctl"][
        "env"
    ]["FAASM_VERSION"]


def get_version():
    """
    Get version for the examples repository

    The version depends only on the version of the different cross-compilation
    toolchains we use, in this case CPP and Python
    """
    return "{}_{}".format(get_cpp_version(), get_python_version())


def in_docker():
    return "IN_DOCKER" in environ
