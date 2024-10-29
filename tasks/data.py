from faasmctl.util.upload import upload_file
from invoke import task
from tasks.env import EXAMPLES_DATA_FILES


@task(default=True)
def upload(ctx):
    """
    Upload shared files needed to run WASM examples
    """
    for p in EXAMPLES_DATA_FILES:
        host_path = p[0]
        faasm_path = p[1]

        upload_file(host_path, faasm_path)
