from faasmtools.build import CMAKE_TOOLCHAIN_FILE, get_faasm_build_env_dict
from faasmtools.env import LLVM_NATIVE_VERSION
from tasks.env import EXAMPLES_DIR
from invoke import task
from os import environ, listdir, makedirs
from os.path import exists, isdir, join
from shutil import copy, rmtree
from subprocess import run


@task(default=True)
def build(
    ctx, clean=False, native=False, migration=False, migration_net=False
):
    """ """
    opencv_dir = join(EXAMPLES_DIR, "opencv")
    if native:
        build_dir = join(opencv_dir, "build", "native")
    else:
        build_dir = join(opencv_dir, "build", "wasm")

    if clean and exists(build_dir):
        rmtree(build_dir)

    if not exists(build_dir):
        makedirs(build_dir)

    cmake_cmd = [
        "cmake",
        "-GNinja",
        "-DCMAKE_BUILD_TYPE=Release",
    ]

    if native:
        llvm_major = LLVM_NATIVE_VERSION.split(".")[0]
        cmake_cmd += [
            "-DCMAKE_C_COMPILER=/usr/bin/clang-{}".format(llvm_major),
            "-DCMAKE_CXX_COMPILER=/usr/bin/clang++-{}".format(llvm_major),
        ]
    else:
        cmake_cmd += [
            "-DCMAKE_TOOLCHAIN_FILE={}".format(CMAKE_TOOLCHAIN_FILE),
        ]

    # Common flags. Need to be very restrictive for WASM, but we do the same
    # for native
    cmake_cmd += [
        "-DBUILD_LIST=core,imgcodecs,imgproc,ml",
        "-DBUILD_SHARED_LIBS=OFF",
        "-DENABLE_PIC=FALSE",
        "-DCMAKE_BUILD_TYPE=Release",
        "-DCPU_BASELINE=''",
        "-DCPU_DISPATCH=''",
        "-DCV_TRACE=OFF",
        "-DWITH_1394=OFF",
        "-DWITH_ADE=OFF",
        "-DWITH_VTK=OFF",
        "-DWITH_EIGEN=OFF",
        "-DWITH_FFMPEG=OFF",
        "-DWITH_GSTREAMER=OFF",
        "-DWITH_GTK=OFF",
        "-DWITH_GTK_2_X=OFF",
        "-DWITH_IPP=OFF",
        "-DWITH_JASPER=OFF",
        "-DWITH_JPEG=OFF",
        "-DWITH_WEBP=OFF",
        "-DWITH_OPENJPEG=OFF",
        "-DWITH_OPENEXR=OFF",
        "-DWITH_OPENGL=OFF",
        "-DWITH_OPENVX=OFF",
        "-DWITH_OPENNI=OFF",
        "-DWITH_OPENNI2=OFF",
        "-DWITH_PNG=OFF",
        "-DWITH_PTHREADS=OFF",
        "-DWITH_TBB=OFF",
        "-DWITH_TIFF=OFF",
        "-DWITH_V4L=OFF",
        "-DWITH_OPENCL=OFF",
        "-DWITH_OPENCL_SVM=OFF",
        "-DWITH_OPENCLAMDFFT=OFF",
        "-DWITH_OPENCLAMDBLAS=OFF",
        "-DWITH_GPHOTO2=OFF",
        "-DWITH_LAPACK=OFF",
        "-DWITH_ITT=OFF",
        "-DWITH_QUIRC=OFF",
        # Enable SIMD support
        "-DCV_ENABLE_INTRINSICS=ON",
        # Disable threading: problems with SGX,
        "-DOPENCV_DISABLE_THREAD_SUPPORT=ON",
        "-DWITH_IPP=OFF",
        "-DWITH_TBB=OFF",
        "-DWITH_PTHREADS_PF=OFF",
        "-DENABLE_PTHREADS=OFF",
    ]
    cmake_cmd += [opencv_dir]
    cmake_cmd = " ".join(cmake_cmd)

    work_env = environ.copy()
    if not native:
        work_env.update(get_faasm_build_env_dict())

    print(cmake_cmd)
    run(cmake_cmd, shell=True, check=True, cwd=build_dir, env=work_env)
    run("ninja", shell=True, check=True, cwd=build_dir)

    if not native:
        # Manually install headers and libraries
        header_dirs = [
            "include",
            "build/wasm",
            "modules/core/include",
            "modules/calib3d/include",
            "modules/features2d/include",
            "modules/flann/include",
            "modules/imgcodecs/include",
            "modules/imgproc/include",
            "modules/ml/include",
            "modules/photo/include",
            "modules/video/include",
        ]
        dst_header_dir = join(
            work_env["FAASM_WASM_HEADER_INSTALL_DIR"], "opencv2"
        )
        makedirs(dst_header_dir, exist_ok=True)
        for header_dir in header_dirs:
            for header_file in listdir(
                join(opencv_dir, header_dir, "opencv2")
            ):
                src_path = join(opencv_dir, header_dir, "opencv2", header_file)
                dst_path = join(dst_header_dir, header_file)
                if isdir(src_path):
                    run(
                        f"cp -r {src_path} {dst_header_dir}",
                        shell=True,
                        check=True,
                    )
                else:
                    copy(src_path, dst_path)

        for lib_name in listdir(join(build_dir, "lib")):
            copy(
                join(build_dir, "lib", lib_name),
                join(work_env["FAASM_WASM_LIB_INSTALL_DIR"], lib_name),
            )
