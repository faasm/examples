set(FAASM_USER tflite)

set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} --target=$ENV{FAASM_WASM_TRIPLE} -pthread")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} --target=$ENV{FAASM_WASM_TRIPLE} -pthread")
set(CMAKE_EXE_LINKER_FLAGS "$ENV{FAASM_WASM_EXE_LINKER_FLAGS}")

set(TF_LIB libtensorflow-lite.a)

faasm_example_func(image image.cpp)

set(TF_HEADERS
    $ENV{FAASM_WASM_HEADER_INSTALL_DIR}/tensorflow
    $ENV{FAASM_WASM_HEADER_INSTALL_DIR}/tensorflow/tensorflow/lite/tools/make/downloads/flatbuffers/include
)

target_include_directories(tf_check PUBLIC ${TF_HEADERS})
target_link_libraries(tf_check ${TF_LIB})
