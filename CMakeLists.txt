cmake_minimum_required(VERSION 3.4...3.18)
project(geometry LANGUAGES CXX)

add_subdirectory(pybind11)

find_package(Python COMPONENTS Interpreter Development REQUIRED)

include_directories(metacity/cxxgeometry)
link_directories(metacity/cxxgeometry)

#add_compile_options(-std=c++17 -Wall -pedantic -O3) #-g -fsanitize=address -fno-omit-frame-pointer -shared-libasan)
#add_link_options(-fsanitize=address -shared-libasan)

pybind11_add_module(${PROJECT_NAME} metacity/cxxgeometry/geometry.cpp 
                                    metacity/cxxgeometry/primitives.cpp 
                                    metacity/cxxgeometry/primitives.hpp 
                                    metacity/cxxgeometry/points.cpp
                                    metacity/cxxgeometry/points.hpp
                                    metacity/cxxgeometry/lines.cpp
                                    metacity/cxxgeometry/lines.hpp
                                    metacity/cxxgeometry/polygons.cpp
                                    metacity/cxxgeometry/polygons.hpp
                                    metacity/cxxgeometry/triangulation.cpp
                                    metacity/cxxgeometry/triangulation.hpp
                                    metacity/cxxgeometry/slicing.cpp
                                    metacity/cxxgeometry/slicing.hpp
                                    metacity/cxxgeometry/bbox.hpp
                                    metacity/cxxgeometry/bbox.cpp
                                    metacity/cxxgeometry/types.cpp
                                    metacity/cxxgeometry/types.hpp
                                    metacity/cxxgeometry/attributes.cpp
                                    metacity/cxxgeometry/attributes.hpp
                                    metacity/cxxgeometry/rtree.hpp
                                    metacity/cxxgeometry/rtree.cpp
                                    metacity/cxxgeometry/cgal.hpp)


find_package(Eigen3 CONFIG REQUIRED)
target_link_libraries(${PROJECT_NAME} PRIVATE Eigen3::Eigen)

find_package(CGAL CONFIG COMPONENTS REQUIRED)
target_link_libraries(${PROJECT_NAME} PRIVATE CGAL::CGAL)
