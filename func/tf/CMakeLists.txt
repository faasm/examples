set(FAASM_USER tf)

set(TF_LIB ${CMAKE_SYSROOT}/lib/wasm32-wasi/libtensorflow-lite.a)

faasm_example_func(check check.cpp)

set(TF_HEADERS
    ${CMAKE_SYSROOT}/include/tensorflow
    ${CMAKE_SYSROOT}/include/tensorflow/tensorflow/lite/tools/make/downloads/flatbuffers/include
)

target_include_directories(tf_check PUBLIC ${TF_HEADERS})
target_link_libraries(tf_check ${TF_LIB})
