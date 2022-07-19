cmake_minimum_required(VERSION 3.4...3.18)
project(geometry LANGUAGES CXX)
set (CMAKE_CXX_STANDARD 17)

add_subdirectory(pybind11)

find_package(Python COMPONENTS Interpreter Development REQUIRED)

include_directories(metacity/geometry)
link_directories(metacity/geometry)

add_compile_options(-Wall -pedantic -O3 -lpthreads) #-fsanitize=address -fno-omit-frame-pointer -shared-libasan)
#add_link_options(-fsanitize=address -shared-libasan)


pybind11_add_module(${PROJECT_NAME} metacity/geometry/geometry.cpp 
                                    metacity/geometry/progress.hpp 
                                    metacity/geometry/model.cpp 
                                    metacity/geometry/model.hpp 
                                    metacity/geometry/layer.cpp 
                                    metacity/geometry/layer.hpp 
                                    metacity/geometry/attribute.cpp 
                                    metacity/geometry/attribute.hpp 
                                    metacity/geometry/types.hpp
                                    metacity/geometry/grid.cpp
                                    metacity/geometry/grid.hpp
                                    metacity/geometry/triangulation.cpp
                                    metacity/geometry/triangulation.hpp)


