cmake_minimum_required(VERSION 3.10.0)
project(py_libsudoku)

set (CMAKE_EXPORT_COMPILE_COMMANDS ON)

add_subdirectory(pybind11)
add_subdirectory(libsudoku)

include_directories(libsudoku/src)

pybind11_add_module(py_libsudoku src/py_libsudoku.cpp)
target_link_libraries(py_libsudoku PRIVATE libsudoku_objs)
set_target_properties(py_libsudoku
    PROPERTIES
      OUTPUT_NAME "py_libsudoku"
)

