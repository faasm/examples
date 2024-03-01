set(FAASM_USER tf)

set(TF_LIB libtensorflow-lite.a)

faasm_example_func(check check.cpp)

set(TF_HEADERS
    $ENV{FAASM_WASM_HEADER_INSTALL_DIR}/tensorflow
    $ENV{FAASM_WASM_HEADER_INSTALL_DIR}/tensorflow/tensorflow/lite/tools/make/downloads/flatbuffers/include
)

target_include_directories(tf_check PUBLIC ${TF_HEADERS})
target_link_libraries(tf_check ${TF_LIB})
