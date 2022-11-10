from faasmtools.env import get_version as get_cpp_version
from faasmtools.docker import (
    build_container,
    push_container,
)
from tasks.env import (
    PROJ_ROOT,
    get_python_version,
    get_version,
)
from invoke import task
from os.path import join

EXAMPLES_IMAGE_NAME = "faasm/examples"
EXAMPLES_DOCKERFILE = join(PROJ_ROOT, "Dockerfile")


def get_tag():
    version = get_version()
    return "{}:{}".format(EXAMPLES_IMAGE_NAME, version)


def build(ctx, nocache=False, push=False):
    """
    Build container image.
    """
    build_args = {
        "CPP_VERSION": get_cpp_version(),
        "EXAMPLES_VERSION": get_version(),
        "PYTHON_VERSION": get_python_version(),
    }

    build_container(
        get_tag(),
        EXAMPLES_DOCKERFILE,
        PROJ_ROOT,
        nocache=nocache,
        push=push,
        build_args=build_args,
    )


@task(iterable=["c"])
def push(ctx, c):
    """
    Push container image.
    """
    push_container(get_tag())
