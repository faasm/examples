from faasmtools.env import WASM_DIR
from invoke import task
from os import environ, makedirs
from os.path import exists, join
from shutil import rmtree
from subprocess import run
from tasks.env import (
    DEV_FAASM_LOCAL,
    EXAMPLES_BUILD_IMAGE_NAME,
    PROJ_ROOT,
    get_faasm_version,
    get_version,
)


@task(default=True)
def cli(ctx, service, clean=False):
    """
    Get a shell into one of the containers: `build` or `run`
    """
    if clean:
        # Clean existing build
        if exists(DEV_FAASM_LOCAL):
            rmtree(DEV_FAASM_LOCAL)
        makedirs(DEV_FAASM_LOCAL)

        # Populate the local mounts with the existing content
        tmp_ctr_name = "examples-build"
        docker_cmd = "docker run -i -d --name {} {}:{}".format(
            tmp_ctr_name, EXAMPLES_BUILD_IMAGE_NAME, get_version()
        )
        run(docker_cmd, shell=True, check=True)
        run(
            "docker cp examples-build:{} {}".format(
                WASM_DIR, join(DEV_FAASM_LOCAL, "wasm")
            ),
            shell=True,
            check=True,
        )
        run("docker rm -f {}".format(tmp_ctr_name), shell=True, check=True)

    build_env = environ.copy()
    build_env.update(
        {
            "EXAMPLES_RUN_VERSION": get_faasm_version(),
            "EXAMPLES_BUILD_VERSION": get_version(),
        }
    )
    docker_cmd = "docker compose up -d --no-recreate"
    run(docker_cmd, shell=True, check=True, cwd=PROJ_ROOT, env=build_env)

    docker_cmd = "docker compose exec -it {} bash".format(service)
    run(docker_cmd, shell=True, check=True, cwd=PROJ_ROOT, env=build_env)


@task()
def stop(ctx):
    build_env = environ.copy()
    build_env.update(
        {
            "EXAMPLES_RUN_VERSION": get_faasm_version(),
            "EXAMPLES_BUILD_VERSION": get_version(),
        }
    )
    run(
        "docker compose down",
        shell=True,
        check=True,
        cwd=PROJ_ROOT,
        env=build_env,
    )
