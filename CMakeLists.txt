cmake_minimum_required(VERSION 3.4...3.18)
project(primitive LANGUAGES CXX)

set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/metacity/geometry)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/metacity/geometry)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/metacity/geometry)
#set(CMAKE_BUILD_TYPE Debug)
set(CMAKE_BUILD_TYPE Release)

set(pybind11_DIR "env/lib/python3.9/site-packages/pybind11/share/cmake/pybind11")
find_package(Python COMPONENTS Interpreter Development REQUIRED)
find_package(pybind11 CONFIG REQUIRED)
find_package(CGAL REQUIRED COMPONENTS)

include_directories(metacity/geometry)
link_directories(metacity/geometry)

add_compile_options(-std=c++17 -Wall -pedantic -O3) #-g -fsanitize=address -fno-omit-frame-pointer -shared-libasan)
#add_link_options(-fsanitize=address -shared-libasan)

pybind11_add_module(${PROJECT_NAME} metacity/geometry/primitive.cpp 
                                    metacity/geometry/primitives.cpp 
                                    metacity/geometry/primitives.hpp 
                                    metacity/geometry/points.cpp
                                    metacity/geometry/points.hpp
                                    metacity/geometry/lines.cpp
                                    metacity/geometry/lines.hpp
                                    metacity/geometry/polygons.cpp
                                    metacity/geometry/polygons.hpp
                                    metacity/geometry/triangulation.cpp
                                    metacity/geometry/triangulation.hpp
                                    metacity/geometry/slicing.cpp
                                    metacity/geometry/slicing.hpp
                                    metacity/geometry/types.cpp
                                    metacity/geometry/types.hpp
                                    metacity/geometry/attributes.cpp
                                    metacity/geometry/attributes.hpp
                                    metacity/geometry/rtree.hpp
                                    metacity/geometry/rtree.cpp
                                    metacity/geometry/cgal.hpp)

target_compile_definitions(${PROJECT_NAME} PUBLIC)

find_package(Eigen3 CONFIG REQUIRED)
target_link_libraries(${PROJECT_NAME} PRIVATE Eigen3::Eigen)

find_package(CGAL CONFIG REQUIRED)
target_link_libraries(${PROJECT_NAME} PRIVATE CGAL::CGAL)
