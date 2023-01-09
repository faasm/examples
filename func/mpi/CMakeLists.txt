set(FAASM_USER mpi)

set(OMPI_CXX ${CXX})
set(OMPI_C ${C})

function(mpi_func exec_name dir_path)
    faasm_example_func(${exec_name} ${dir_path})

    target_link_libraries(${FAASM_USER}_${exec_name} faasmpi mpi)

    if (NOT CMAKE_SYSTEM_NAME STREQUAL "Wasm")
        target_link_libraries(${FAASM_USER}_${exec_name} pthread)
    endif ()
endfunction(mpi_func)

mpi_func(migrate migrate.cpp)
