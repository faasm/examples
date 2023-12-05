from faasmtools.docker import ACR_NAME
from faasmtools.env import get_version as get_cpp_version
from os.path import dirname, abspath, join
from re import search as re_search
from subprocess import run

PROJ_ROOT = dirname(dirname(abspath(__file__)))
DOCKER_ROOT = join(PROJ_ROOT, "docker")
EXAMPLES_DIR = join(PROJ_ROOT, "examples")
DEV_FAASM_LOCAL = join(PROJ_ROOT, "dev", "faasm-local")
WASM_DIR = join(PROJ_ROOT, "wasm")

# Docker variables
EXAMPLES_BUILD_IMAGE_NAME = "{}/examples-build".format(ACR_NAME)
EXAMPLES_BUILD_DOCKERFILE = join(DOCKER_ROOT, "build.dockerfile")
EXAMPLES_RUN_IMAGE_NAME = "{}/examples-run".format(ACR_NAME)
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
    ver_file = join(PROJ_ROOT, "FAASM_VERSION")

    with open(ver_file, "r") as fh:
        version = fh.read()

    version = version.strip()
    return version


def get_faabric_version(old_faasm_ver, new_faasm_ver):
    """
    Get the faabric version by `wget`-ing the FAASM version file for the tagged
    Faasm version
    """
    def do_get_ver(faasm_ver):
        tmp_file = "/tmp/faabric_version"
        wget_cmd = [
            "wget",
            "-O {}".format(tmp_file),
            "https://raw.githubusercontent.com/faasm/faasm/v{}/.env".format(faasm_ver),
        ]
        wget_cmd = " ".join(wget_cmd)
        out = run(wget_cmd, shell=True, capture_output=True)
        assert out.returncode == 0

        with open(tmp_file, "r") as fh:
            ver = re_search(r"planner:([0-9\.]*)", fh.read()).groups(1)[0]

        return ver

    return do_get_ver(old_faasm_ver), do_get_ver(new_faasm_ver)


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
