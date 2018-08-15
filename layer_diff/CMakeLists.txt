cmake_minimum_required(VERSION 3.9)
project(layer_compress)

set(CMAKE_CXX_STANDARD 11)

add_executable(layer_compress main.cpp)
target_link_libraries(layer_compress ${CMAKE_CURRENT_SOURCE_DIR}/lib/FastPFor/libFastPFor.a)
