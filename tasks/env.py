from faasmtools.env import get_version as get_cpp_version
from os.path import dirname, abspath, join

PROJ_ROOT = dirname(dirname(abspath(__file__)))
EXAMPLES_DIR = join(PROJ_ROOT, "examples")


def get_python_version():
    """
    Get the version of the python submodule
    """
    ver_file = join(PROJ_ROOT, "python", "VERSION")

    with open(ver_file, "r") as fh:
        version = fh.read()

    version = version.strip()
    return version


def get_version():
    """
    Get version for the examples repository

    The version depends only on the version of the different cross-compilation
    toolchains we use, in this case CPP and Python
    """
    return "{}_{}".format(get_cpp_version(), get_python_version())
