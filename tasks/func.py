from faasmtools.compile_util import wasm_cmake, wasm_copy_upload
from invoke import task
from os.path import join
from tasks.env import PROJ_ROOT

FUNC_DIR = join(PROJ_ROOT, "func")
FUNC_BUILD_DIR = join(PROJ_ROOT, "build", "func")


def _copy_built_function(user, func):
    exe_name = "{}_{}.{}".format(user, func, "wasm")
    src_file = join(FUNC_BUILD_DIR, user, exe_name)
    wasm_copy_upload(user, func, src_file)


@task(default=True)
def compile(ctx, user, func, clean=False, debug=False):
    """
    Compile a function to test a sample library
    """
    # Build the function (gets written to the build dir)
    wasm_cmake(FUNC_DIR, FUNC_BUILD_DIR, "{}_{}".format(user, func), clean, debug)

    # Copy into place
    _copy_built_function(user, func)
