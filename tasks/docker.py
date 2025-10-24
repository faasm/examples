from faasmtools.env import get_version as get_cpp_version
from faasmtools.docker import (
    build_container,
    push_container,
)
from tasks.env import (
    EXAMPLES_BASE_DOCKERFILE,
    EXAMPLES_BASE_IMAGE_NAME,
    EXAMPLES_BUILD_DOCKERFILE,
    EXAMPLES_BUILD_IMAGE_NAME,
    DOCKER_ROOT,
    get_python_version,
    get_version,
)
from invoke import task


def get_tag(c):
    image_name = (
        EXAMPLES_BUILD_IMAGE_NAME if c == "build" else EXAMPLES_BASE_IMAGE_NAME
    )
    return "{}:{}".format(image_name, get_version())


@task(iterable=["ctr"])
def build(ctx, ctr, nocache=False, push=False):
    """
    Build container image. Must be one in: `build`, `base`
    """
    for c in ctr:
        if c == "build":
            build_args = {
                "CPP_VERSION": get_cpp_version(),
                "EXAMPLES_VERSION": get_version(),
                "PYTHON_VERSION": get_python_version(),
            }

            dockerfile = EXAMPLES_BUILD_DOCKERFILE
        elif c == "base":
            build_args = {
                "OPENMPI_VERSION": "4.1.0",
                "OPENMPI_VERSION_NOPATCH": "4.1",
            }

            dockerfile = EXAMPLES_BASE_DOCKERFILE
        else:
            raise RuntimeError("Unrecognised container name: {}".format(c))

        build_container(
            get_tag(c),
            dockerfile,
            DOCKER_ROOT,
            nocache=nocache,
            push=push,
            build_args=build_args,
        )


@task(iterable=["ctr"])
def push(ctx, ctr):
    """
    Push container image
    """
    for c in ctr:
        push_container(get_tag(c))
