set(FAASM_USER ffmpeg)

# FFmpeg build
set(FFMPEG_INCLUDE_DIRS
    $ENV{FAASM_WASM_HEADER_INSTALL_DIR}/libavcodec
    $ENV{FAASM_WASM_HEADER_INSTALL_DIR}/libavformat
)
set(FFMPEG_LIBS
    $ENV{FAASM_WASM_LIB_INSTALL_DIR}/libavcodec.a
    $ENV{FAASM_WASM_LIB_INSTALL_DIR}/libavformat.a
    $ENV{FAASM_WASM_LIB_INSTALL_DIR}/libavutil.a
    $ENV{FAASM_WASM_LIB_INSTALL_DIR}/libswscale.a
    $ENV{FAASM_WASM_LIB_INSTALL_DIR}/libswresample.a
)

faasm_example_func(check check.cpp)

target_include_directories(ffmpeg_check PUBLIC ${FFMPEG_INCLUDE_DIRS})
target_link_libraries(ffmpeg_check ${FFMPEG_LIBS})
