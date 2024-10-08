from faasmtools.build import FAASM_LOCAL_DIR
from invoke import task
from os import environ, makedirs
from os.path import exists
from shutil import rmtree
from subprocess import run
from tasks.env import (
    DEV_FAASM_LOCAL,
    EXAMPLES_BUILD_IMAGE_NAME,
    PROJ_ROOT,
    get_version,
)


@task(default=True)
def cli(ctx, clean=False):
    """
    Get a shell into the examples build container
    """
    service = "build"

    if not exists(DEV_FAASM_LOCAL) or clean:
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
            "docker cp examples-build:{}/. {}".format(
                FAASM_LOCAL_DIR, DEV_FAASM_LOCAL
            ),
            shell=True,
            check=True,
        )
        run("docker rm -f {}".format(tmp_ctr_name), shell=True, check=True)

    build_env = environ.copy()
    build_env.update({"EXAMPLES_BUILD_VERSION": get_version()})
    docker_cmd = "docker compose up -d --no-recreate {}".format(service)
    run(docker_cmd, shell=True, check=True, cwd=PROJ_ROOT, env=build_env)

    docker_cmd = "docker compose exec -it {} bash".format(service)
    run(docker_cmd, shell=True, check=True, cwd=PROJ_ROOT, env=build_env)


@task()
def stop(ctx):
    build_env = environ.copy()
    build_env.update({"EXAMPLES_BUILD_VERSION": get_version()})
    run(
        "docker compose down",
        shell=True,
        check=True,
        cwd=PROJ_ROOT,
        env=build_env,
    )
