from faasmtools.build import FAASM_LOCAL_DIR
from invoke import task
from os import makedirs
from os.path import basename, exists, join
from shutil import copyfile
from tasks.env import EXAMPLES_DIR

DATA_BASE_DIR = join(FAASM_LOCAL_DIR, "shared")


@task(default=True)
def prepare(ctx):
    """
    Prepare data files to test WASM examples
    """
    data_files = [
        [
            join(
                EXAMPLES_DIR,
                "lammps",
                "examples",
                "controller",
                "in.controller.wall",
            ),
            join(DATA_BASE_DIR, "lammps-data", "in.controller.wall"),
        ]
    ]

    for p in data_files:
        path_src = p[0]
        path_dst = p[1]

        if not exists(basename(path_dst)):
            makedirs(basename(path_dst))

        copyfile(path_src, path_dst)
