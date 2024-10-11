set(FAASM_USER opencv)

faasm_example_func(check check.cpp)

target_link_libraries(opencv_check opencv_core opencv_imgcodecs opencv_imgproc)
