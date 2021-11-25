cmake_minimum_required(VERSION 3.4...3.18)
project(geometry LANGUAGES CXX)

add_subdirectory(pybind11)

find_package(Python COMPONENTS Interpreter Development REQUIRED)

include_directories(metacity/geometrycpp)
link_directories(metacity/geometrycpp)

add_compile_options(-std=c++17 -Wall -pedantic -O3)#-g -fsanitize=address -fno-omit-frame-pointer -shared-libasan)
#add_link_options(-fsanitize=address -shared-libasan)

pybind11_add_module(${PROJECT_NAME} metacity/geometrycpp/geometry.cpp 
                                    metacity/geometrycpp/models.cpp 
                                    metacity/geometrycpp/models.hpp 
                                    metacity/geometrycpp/timepoints.cpp
                                    metacity/geometrycpp/timepoints.hpp
                                    metacity/geometrycpp/points.cpp
                                    metacity/geometrycpp/points.hpp
                                    metacity/geometrycpp/lines.cpp
                                    metacity/geometrycpp/lines.hpp
                                    metacity/geometrycpp/polygons.cpp
                                    metacity/geometrycpp/polygons.hpp
                                    metacity/geometrycpp/triangulation.cpp
                                    metacity/geometrycpp/triangulation.hpp
                                    metacity/geometrycpp/slicing.cpp
                                    metacity/geometrycpp/slicing.hpp
                                    metacity/geometrycpp/bbox.hpp
                                    metacity/geometrycpp/bbox.cpp
                                    metacity/geometrycpp/types.cpp
                                    metacity/geometrycpp/types.hpp
                                    metacity/geometrycpp/attributes.cpp
                                    metacity/geometrycpp/attributes.hpp
                                    metacity/geometrycpp/rtree.hpp
                                    metacity/geometrycpp/rtree.cpp
                                    metacity/geometrycpp/bvh.hpp
                                    metacity/geometrycpp/bvh.cpp
                                    metacity/geometrycpp/png.hpp
                                    metacity/geometrycpp/png.cpp
                                    metacity/geometrycpp/legobuilder.hpp
                                    metacity/geometrycpp/legobuilder.cpp
                                    metacity/geometrycpp/interval.cpp
                                    metacity/geometrycpp/interval.hpp
                                    metacity/geometrycpp/cgal.hpp)


find_package(CGAL CONFIG COMPONENTS REQUIRED)
target_link_libraries(${PROJECT_NAME} PRIVATE CGAL::CGAL)
