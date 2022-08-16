cmake_minimum_required(VERSION 3.4...3.18)
project(geometry LANGUAGES CXX)
set (CMAKE_CXX_STANDARD 17)

add_subdirectory(pybind11)

find_package(Python COMPONENTS Interpreter Development REQUIRED)

include_directories(metacity/geometry)
link_directories(metacity/geometry)

add_compile_options(-Wall -pedantic -g) 
#add_compile_options(-Wall -pedantic -O3)
#add_link_options(-fsanitize=address -shared-libasan -pthread)
add_link_options(-pthread)


pybind11_add_module(${PROJECT_NAME} metacity/geometry/geometry.cpp 
                                    metacity/geometry/types.hpp
                                    metacity/geometry/convert.hpp
                                    metacity/geometry/progress.hpp 
                                    metacity/geometry/mesh_pipeline/bbox.hpp 
                                    metacity/geometry/mesh_pipeline/bbox.cpp 
                                    metacity/geometry/mesh_pipeline/modifiers.hpp 
                                    metacity/geometry/mesh_pipeline/modifiers.cpp 
                                    metacity/geometry/mesh_pipeline/graham.hpp 
                                    metacity/geometry/mesh_pipeline/graham.cpp 
                                    metacity/geometry/mesh_pipeline/bvh.hpp 
                                    metacity/geometry/mesh_pipeline/bvh.cpp 
                                    metacity/geometry/mesh_pipeline/model.hpp 
                                    metacity/geometry/mesh_pipeline/model.cpp 
                                    metacity/geometry/mesh_pipeline/layer.hpp 
                                    metacity/geometry/mesh_pipeline/layer.cpp 
                                    metacity/geometry/mesh_pipeline/attribute.hpp 
                                    metacity/geometry/mesh_pipeline/attribute.cpp 
                                    metacity/geometry/mesh_pipeline/grid.hpp
                                    metacity/geometry/mesh_pipeline/grid.cpp
                                    metacity/geometry/mesh_pipeline/triangulation.hpp
                                    metacity/geometry/mesh_pipeline/triangulation.cpp
                                    metacity/geometry/vector_pipeline/graph.hpp
                                    metacity/geometry/vector_pipeline/graph.cpp)


