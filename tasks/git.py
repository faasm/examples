from invoke import task
from subprocess import run
from tasks.env import (
    EXAMPLES_BUILD_IMAGE_NAME,
    PROJ_ROOT,
    get_faasm_version,
    get_version,
)

VERSIONED_FILES = {
    "faasm": ["FAASM_VERSION", ".github/workflows/tests.yml"],
    "cpp": [".github/workflows/tests.yml"],
    "python": [".github/workflows/tests.yml"],
}


@task
def tag(ctx, force=False):
    """
    Creates git tag from the current tree
    """
    version = get_version()
    tag_name = "v{}".format(version)
    run(
        "git tag {} {}".format("--force" if force else "", tag_name),
        shell=True,
        check=True,
        cwd=PROJ_ROOT,
    )

    run(
        "git push {} origin {}".format("--force" if force else "", tag_name),
        shell=True,
        check=True,
        cwd=PROJ_ROOT,
    )


@task
def bump(ctx, submodule, ver=None):
    """
    Bump a submodule's dependency: `faasm`, `cpp`, or `python`
    """
    allowed_submodules = ["faasm", "cpp", "python"]
    if submodule not in allowed_submodules:
        print("Unrecognised submodule: {}".format(allowed_submodules))
        print("Submodule must be one in: {}".format(allowed_submodules))
        raise RuntimeError("Unrecognised submodule")

    if submodule == "faasm":
        old_ver = get_faasm_version()
        if ver:
            new_ver = ver
        else:
            # Just bump the last minor version part
            new_ver_parts = old_ver.split(".")
            new_ver_minor = int(new_ver_parts[-1]) + 1
            new_ver_parts[-1] = str(new_ver_minor)
            new_ver = ".".join(new_ver_parts)

        # Replace version in all files
        for f in VERSIONED_FILES["faasm"]:
            sed_cmd = "sed -i 's/{}/{}/g' {}".format(old_ver, new_ver, f)
            run(sed_cmd, shell=True, check=True)
    else:
        new_ver = get_version("build")
        grep_cmd = "grep '{}' .github/workflows/tests.yml".format(
            EXAMPLES_BUILD_IMAGE_NAME
        )
        old_ver = (
            run(grep_cmd, shell=True, cwd=PROJ_ROOT, capture_output=True)
            .stdout.decode("utf-8")
            .strip()
            .split(":")[-1]
        )

        # Replace version in all files
        for f in VERSIONED_FILES[submodule]:
            sed_cmd = "sed -i 's/{}/{}/g' {}".format(old_ver, new_ver, f)
            run(sed_cmd, shell=True, check=True)
