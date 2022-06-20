cmake_minimum_required(VERSION 3.4...3.18)
project(geometry LANGUAGES CXX)
set (CMAKE_CXX_STANDARD 17)

add_subdirectory(pybind11)

find_package(Python COMPONENTS Interpreter Development REQUIRED)

include_directories(metacity/geometrycpp)
link_directories(metacity/geometrycpp)

add_compile_options(-Wall -pedantic -O3) #-fsanitize=address -fno-omit-frame-pointer -shared-libasan)
#add_link_options(-fsanitize=address -shared-libasan)


pybind11_add_module(${PROJECT_NAME} metacity/geometrycpp/geometry.cpp 
                                    metacity/geometrycpp/models.cpp 
                                    metacity/geometrycpp/models.hpp 
                                    metacity/geometrycpp/attribute.cpp 
                                    metacity/geometrycpp/attribute.hpp 
                                    metacity/geometrycpp/types.hpp
                                    metacity/geometrycpp/triangulation.cpp
                                    metacity/geometrycpp/triangulation.hpp)


