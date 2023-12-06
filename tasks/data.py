from invoke import task
from os import makedirs
from os.path import dirname, exists
from shutil import copyfile
from tasks.env import EXAMPLES_DATA_FILES


@task(default=True)
def prepare(ctx):
    """
    Prepare data files to test WASM examples
    """
    for p in EXAMPLES_DATA_FILES:
        path_src = p[0]
        path_dst = p[1]

        if not exists(dirname(path_dst)):
            makedirs(dirname(path_dst))

        copyfile(path_src, path_dst)
