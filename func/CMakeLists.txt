cmake_minimum_required(VERSION 3.8.0)
project(faasm-examples-func)

# -----------------------------------------
# Most of the variables used transitively used here like compiler or linker
# flags are set in the sysroot file (WasiToolchain.cmake) and are defined in
# the build environment file (faasmtools/build.py)
# -----------------------------------------

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# For Faasm functions, we add `_faasm_zygote` as an exported symbol
set(CMAKE_EXE_LINKER_FLAGS
    "${CMAKE_EXE_LINKER_FLAGS} -Xlinker --export=_faasm_zygote"
)
message(STATUS "Detected wasm build (sysroot=$ENV{FAASM_WASM_SYSROOT})")
set(CMAKE_EXECUTABLE_SUFFIX ".wasm")


set(FAASM_FUNC_LIBS faasm c-printscan-long-double)

function(faasm_example_func_c func_name file_name)
    add_executable(${func_name} ${file_name})
    target_link_libraries(${func_name} ${FAASM_FUNC_LIBS})
endfunction(faasm_example_func_c)

function(faasm_example_func func_name file_name)
    set(target_name "${FAASM_USER}_${func_name}")
    add_executable(${target_name} ${file_name})
    target_link_libraries(${target_name} ${FAASM_FUNC_LIBS})
endfunction(faasm_example_func)

add_subdirectory(ffmpeg)
add_subdirectory(tf)
