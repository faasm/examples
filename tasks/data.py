from faasmtools.build import FAASM_LOCAL_DIR
from invoke import task
from os import makedirs
from os.path import dirname, exists, join
from shutil import copyfile
from tasks.env import EXAMPLES_DIR, PROJ_ROOT

DATA_BASE_DIR = join(FAASM_LOCAL_DIR, "shared")
DATA_HOST_DIR = join(PROJ_ROOT, "data")


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
        ],
        [
            join(DATA_HOST_DIR, "ffmpeg_video.mp4"),
            join(DATA_BASE_DIR, "ffmpeg", "sample_video.mp4"),
        ]
    ]

    for p in data_files:
        path_src = p[0]
        path_dst = p[1]

        if not exists(dirname(path_dst)):
            makedirs(dirname(path_dst))

        copyfile(path_src, path_dst)
