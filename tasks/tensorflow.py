from faasmtools.build import (
    build_config_cmd,
    get_faasm_build_env_dict,
)
from invoke import task
from os import cpu_count
from os.path import exists, isfile, join
from subprocess import check_output, run
from shutil import copytree, rmtree
from tasks.env import EXAMPLES_DIR


@task(default=True)
def lite(ctx, clean=False):
    """
    Compile and install Tensorflow Lite lib
    """
    tf_dir = join(EXAMPLES_DIR, "tensorflow")
    tf_lite_dir = join(tf_dir, "tensorflow", "lite")
    tf_make_dir = join(tf_lite_dir, "tools", "make")

    download_check_dir = join(tf_make_dir, "downloads", "absl")
    if not exists(download_check_dir):
        download_script = join(tf_make_dir, "download_dependencies.sh")
        check_output(download_script, shell=True)

    cores = cpu_count()
    make_cores = int(cores) - 1

    build_env = get_faasm_build_env_dict()
    make_target = "lib"
    make_cmd = build_config_cmd(
        build_env,
        "make -j {}".format(make_cores),
        conf_args=False,
    )
    make_cmd.extend(
        [
            "MINIMAL_SRCS=",
            "TARGET={}".format(build_env["FAASM_WASM_TRIPLE"]),
            "BUILD_WITH_MMAP=false",
            'LIBS="-lstdc++"',
            '-C "{}"'.format(tf_dir),
            "-f tensorflow/lite/tools/make/Makefile",
        ]
    )

    make_cmd.append(make_target)

    clean_dir = join(
        tf_make_dir, "gen", "{}_x86_64".format(build_env["FAASM_WASM_TRIPLE"])
    )
    if clean and exists(clean_dir):
        rmtree(clean_dir)

    make_cmd = " ".join(make_cmd)
    run(make_cmd, shell=True, check=True, cwd=tf_lite_dir)

    # Install static library
    tf_lib_dir = join(clean_dir, "lib")
    cp_cmd = "cp {}/libtensorflow-lite.a {}/libtensorflow-lite.a".format(
        tf_lib_dir, build_env["FAASM_WASM_LIB_INSTALL_DIR"]
    )
    print(cp_cmd)
    run(cp_cmd, shell=True, check=True)

    # Install header files
    header_install_dir = join(
        build_env["FAASM_WASM_HEADER_INSTALL_DIR"], "tensorflow"
    )
    if exists(header_install_dir):
        rmtree(header_install_dir)

    def ignore_func(d, files):
        return [f for f in files if isfile(join(d, f)) and f[-2:] != ".h"]

    copytree(tf_dir, header_install_dir, ignore=ignore_func)
