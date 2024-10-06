set(FAASM_USER jwt)

faasm_example_func(test test.cpp)
target_link_libraries(jwt_test libtless-jwt-cpp.a libtless-jwt.a)
