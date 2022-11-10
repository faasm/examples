from faasmtools.env import get_version as get_cpp_version
from os.path import dirname, abspath, join

PROJ_ROOT = dirname(dirname(abspath(__file__)))
DOCKER_ROOT = join(PROJ_ROOT, "docker")
EXAMPLES_DIR = join(PROJ_ROOT, "examples")

# Docker variables
EXAMPLES_BUILD_IMAGE_NAME = "faasm/examples-build"
EXAMPLES_BUILD_DOCKERFILE = join(DOCKER_ROOT, "build.dockerfile")
EXAMPLES_RUN_IMAGE_NAME = "faasm/examples-build"
EXAMPLES_RUN_DOCKERFILE = join(DOCKER_ROOT, "run.dockerfile")


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
    Get the version of the python submodule
    """
    return get_submodule_version("faasm")


def get_version(name="build"):
    """
    Get version for the examples repository

    The version depends only on the version of the different cross-compilation
    toolchains we use, in this case CPP and Python, and Faasm
    """
    if name == "build":
        return "{}_{}".format(get_cpp_version(), get_python_version())
    if name == "run":
        return "{}".format(get_faasm_version())
