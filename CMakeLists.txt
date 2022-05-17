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
                                    metacity/geometrycpp/loaders.cpp 
                                    metacity/geometrycpp/loaders.hpp 
                                    metacity/geometrycpp/points.cpp
                                    metacity/geometrycpp/points.hpp
                                    metacity/geometrycpp/segments.cpp
                                    metacity/geometrycpp/segments.hpp
                                    metacity/geometrycpp/mesh.cpp
                                    metacity/geometrycpp/mesh.hpp
                                    metacity/geometrycpp/triangulation.cpp
                                    metacity/geometrycpp/triangulation.hpp
                                    metacity/geometrycpp/bbox.hpp
                                    metacity/geometrycpp/bbox.cpp
                                    metacity/geometrycpp/types.cpp
                                    metacity/geometrycpp/types.hpp
                                    metacity/geometrycpp/attributes.cpp
                                    metacity/geometrycpp/attributes.hpp
                                    metacity/geometrycpp/bvh.hpp
                                    metacity/geometrycpp/bvh.cpp
                                    metacity/geometrycpp/png.hpp
                                    metacity/geometrycpp/png.cpp
                                    metacity/geometrycpp/legobuilder.hpp
                                    metacity/geometrycpp/legobuilder.cpp)


