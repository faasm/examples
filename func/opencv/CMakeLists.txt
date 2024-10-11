set(FAASM_USER opencv)

# set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} --target=$ENV{FAASM_WASM_TRIPLE}")
# set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} --target=$ENV{FAASM_WASM_TRIPLE}")
# set(CMAKE_EXE_LINKER_FLAGS "$ENV{FAASM_WASM_EXE_LINKER_FLAGS}")

faasm_example_func(check check.cpp)

# Update these two to properly install targets
# target_include_directories(opencv_check PUBLIC
#     /code/examples/examples/opencv/include
#     /code/examples/examples/opencv/build/wasm
#     /code/examples/examples/opencv/modules/core/include
#     /code/examples/examples/opencv/modules/calib3d/include
#     /code/examples/examples/opencv/modules/features2d/include/
#     /code/examples/examples/opencv/modules/flann/include
#     /code/examples/examples/opencv/modules/imgproc/include
#     /code/examples/examples/opencv/modules/photo/include
#     /code/examples/examples/opencv/modules/video/include
#     /code/examples/examples/opencv/modules/imgcodecs/include
# )
# target_link_directories(opencv_check PUBLIC /code/examples/examples/opencv/build/wasm/lib)

target_link_libraries(opencv_check opencv_core opencv_imgcodecs opencv_imgproc)
#     libopencv_core.a
#     libopencv_imgcodecs.a
#     libopencv_imgproc.a
# )
