from subprocess import run
from tasks.env import (
    DEV_FAASM_LOCAL,
    EXAMPLES_BUILD_IMAGE_CTR,
    EXAMPLES_BUILD_IMAGE_NAME,
    PROJ_ROOT,
    get_version,
)


def start_docker_build_ctr():
    docker_cmd = [
        "docker run",
        "-td",
        "-v {}:/code/examples".format(PROJ_ROOT),
        "-v {}:{}".format(DEV_FAASM_LOCAL, "/usr/local/faasm"),
        "--name {}".format(EXAMPLES_BUILD_IMAGE_CTR),
        "{}:{}".format(EXAMPLES_BUILD_IMAGE_NAME, get_version()),
    ]

    docker_cmd = " ".join(docker_cmd)
    out = run(docker_cmd, shell=True, capture_output=True)
    assert out.returncode == 0, "Error starting build container: {}".format(
        out.stderr.decode("utf-8")
    )


def stop_docker_build_ctr():
    out = run(
        "docker rm -f {}".format(EXAMPLES_BUILD_IMAGE_CTR),
        shell=True,
        capture_output=True,
    )
    assert out.returncode == 0, "Error stopping build container: {}".format(
        out.stderr.decode("utf-8")
    )


def run_docker_build_cmd(cmd_list, cwd=None, env=None):
    start_docker_build_ctr()

    for cmd in cmd_list:
        docker_cmd = [
            "docker exec",
            "--workdir {}".format(cwd) if cwd is not None else "",
            " ".join(['--env {}="{}"'.format(k, env[k]) for k in env])
            if env is not None
            else "",
            EXAMPLES_BUILD_IMAGE_CTR,
            cmd,
        ]

        docker_cmd = " ".join(docker_cmd)
        run(docker_cmd, shell=True, check=True)

    stop_docker_build_ctr()
