set(FAASM_USER opencv)

faasm_example_func(check check.cpp)
target_link_libraries(opencv_check opencv_core opencv_imgcodecs opencv_imgproc)

faasm_example_func(pca pca.cpp)
target_link_libraries(opencv_pca opencv_core opencv_imgcodecs opencv_imgproc opencv_ml z)
