set(FAASM_USER rabe)

faasm_example_func(test test.cpp)
target_link_libraries(rabe_test librabe-cpp.a librabe.a)
