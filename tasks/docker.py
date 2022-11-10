from faasmtools.env import get_version as get_cpp_version
from faasmtools.docker import (
    build_container,
    push_container,
)
from tasks.env import (
    EXAMPLES_BUILD_DOCKERFILE,
    EXAMPLES_BUILD_IMAGE_NAME,
    EXAMPLES_RUN_DOCKERFILE,
    EXAMPLES_RUN_IMAGE_NAME,
    DOCKER_ROOT,
    get_faasm_version,
    get_python_version,
    get_version,
)
from invoke import task


def get_tag(name):
    version = get_version(name)
    if name == "build":
        image_name = EXAMPLES_BUILD_IMAGE_NAME
    elif name == "run":
        image_name = EXAMPLES_RUN_IMAGE_NAME
    return "{}:{}".format(image_name, version)


@task(iterable=["c"])
def build(ctx, c, nocache=False, push=False):
    """
    Build container image, possible containers are `build` and `run`
    """
    build_args = {}
    for ctr in c:
        if ctr == "build":
            build_args = {
                "CPP_VERSION": get_cpp_version(),
                "EXAMPLES_VERSION": get_version(),
                "PYTHON_VERSION": get_python_version(),
            }
            dockerfile = EXAMPLES_BUILD_DOCKERFILE
        elif ctr == "run":
            build_args = {
                "EXAMPLES_VERSION": get_version(),
                "FAASM_VERSION": get_faasm_version(),
            }
            dockerfile = EXAMPLES_RUN_DOCKERFILE
        else:
            raise RuntimeError("Unrecognised container name: {}".format(ctr))

        build_container(
            get_tag(ctr),
            dockerfile,
            DOCKER_ROOT,
            nocache=nocache,
            push=push,
            build_args=build_args,
        )


@task()
def push(ctx):
    """
    Push container image
    """
    push_container(get_tag())
