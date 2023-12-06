from distutils.dir_util import copy_tree
from faasmctl.util.upload import upload_file, upload_wasm
from invoke import task
from os import listdir, makedirs
from os.path import exists, join
from shutil import copyfile, rmtree
from tasks.env import (
    EXAMPLES_DIR,
    EXAMPLES_DATA_FILES,
    EXAMPLES_DATA_BASE_DIR,
    WASM_DIR,
    PROJ_ROOT,
)


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

    wasm_dirs = [join(EXAMPLES_DIR, "Kernels", "build", "wasm")]
    for wasm_dir in wasm_dirs:
        copy_tree(wasm_dir, WASM_DIR)


@task
def upload(ctx):
    """
    Upload all WASM and shared data to a Faasm cluster
    """
    # TODO: delete this line
    WASM_DIR = join(PROJ_ROOT, "dev", "faasm-local", "wasm")
    if not exists(WASM_DIR):
        print("Expected WASM files to be available in {}".format(WASM_DIR))
        raise RuntimeError("WASM directory not found!")

    # Iterate over all dirs and upload
    for user in listdir(WASM_DIR):
        for name in listdir(join(WASM_DIR, user)):
            wasm_path = join(WASM_DIR, user, name, "function.wasm")
            if exists(wasm_path):
                upload_wasm(user, name, wasm_path)

    # Iterate over all shared data files and upload
    for data_file in EXAMPLES_DATA_FILES:
        host_path = data_file[0]
        faasm_path = data_file[1].removeprefix(EXAMPLES_DATA_BASE_DIR + "/")
        upload_file(host_path, faasm_path)
