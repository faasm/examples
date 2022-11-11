set(FAASM_USER ffmpeg)

# FFmpeg build
set(FFMPEG_INCLUDE_DIRS
    ${CMAKE_SYSROOT}/include/libavcodec
    ${CMAKE_SYSROOT}/include/libavformat
)
set(FFMPEG_LIBS
    ${CMAKE_SYSROOT}/lib/wasm32-wasi/libavcodec.a
    ${CMAKE_SYSROOT}/lib/wasm32-wasi/libavformat.a
    ${CMAKE_SYSROOT}/lib/wasm32-wasi/libavutil.a
    ${CMAKE_SYSROOT}/lib/wasm32-wasi/libswscale.a
    ${CMAKE_SYSROOT}/lib/wasm32-wasi/libswresample.a
)

faasm_example_func(check check.cpp)

target_include_directories(ffmpeg_check PUBLIC ${FFMPEG_INCLUDE_DIRS})
target_link_libraries(ffmpeg_check ${FFMPEG_LIBS})
