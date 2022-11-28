from distutils.dir_util import copy_tree
from invoke import task
from os import makedirs
from os.path import exists, join
from shutil import copyfile, rmtree
from tasks.env import EXAMPLES_DIR, WASM_DIR


@task(default=True)
def copy(ctx, clean=False):
    """
    Copy built WASM files into a project-wide directory for distribution
    """
    if clean and exists(WASM_DIR):
        rmtree(WASM_DIR)

    if not exists(WASM_DIR):
        makedirs(WASM_DIR)

    wasm_files = [
        {
            "src": join(EXAMPLES_DIR, "lammps", "build", "wasm", "lmp"),
            "dst": join(WASM_DIR, "lammps.wasm"),
        },
        {
            "src": join(EXAMPLES_DIR, "LULESH", "build", "wasm", "lulesh2.0"),
            "dst": join(WASM_DIR, "lulesh.wasm"),
        },
    ]
    for wasm_file in wasm_files:
        copyfile(wasm_file["src"], wasm_file["dst"])

    wasm_dirs = [
        join(EXAMPLES_DIR, "Kernels", "build", "wasm")
    ]
    for wasm_dir in wasm_dirs:
        copy_tree(wasm_dir, WASM_DIR)
