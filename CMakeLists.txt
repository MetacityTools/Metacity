cmake_minimum_required(VERSION 3.15...3.22)
project(metacity)
set(CMAKE_CXX_STANDARD 14)


if(SKBUILD)
  # Scikit-Build does not add your site-packages to the search path
  # automatically, so we need to add it _or_ the pybind11 specific directory
  # here.
  execute_process(
    COMMAND "${PYTHON_EXECUTABLE}" -c
            "import pybind11; print(pybind11.get_cmake_dir())"
    OUTPUT_VARIABLE _tmp_dir
    OUTPUT_STRIP_TRAILING_WHITESPACE COMMAND_ECHO STDOUT)
  list(APPEND CMAKE_PREFIX_PATH "${_tmp_dir}")
endif()


# Now we can find pybind11
find_package(pybind11 CONFIG REQUIRED)

#add_compile_options(-Wall -pedantic -g) 
add_compile_options(-Wall -pedantic -O3)
#add_link_options(-fsanitize=address -shared-libasan -pthread)
add_link_options(-pthread)


pybind11_add_module(geometry        src/metacity/geometry/geometry.cpp 
                                    src/metacity/geometry/types.hpp
                                    src/metacity/geometry/convert.hpp
                                    src/metacity/geometry/progress.hpp 
                                    src/metacity/geometry/mesh/bbox.hpp 
                                    src/metacity/geometry/mesh/bbox.cpp 
                                    src/metacity/geometry/mesh/modifiers.hpp 
                                    src/metacity/geometry/mesh/modifiers.cpp 
                                    src/metacity/geometry/mesh/graham.hpp 
                                    src/metacity/geometry/mesh/graham.cpp 
                                    src/metacity/geometry/mesh/bvh.hpp 
                                    src/metacity/geometry/mesh/bvh.cpp 
                                    src/metacity/geometry/mesh/model.hpp 
                                    src/metacity/geometry/mesh/model.cpp 
                                    src/metacity/geometry/mesh/layer.hpp 
                                    src/metacity/geometry/mesh/layer.cpp 
                                    src/metacity/geometry/mesh/attribute.hpp 
                                    src/metacity/geometry/mesh/attribute.cpp 
                                    src/metacity/geometry/mesh/grid.hpp
                                    src/metacity/geometry/mesh/grid.cpp
                                    src/metacity/geometry/mesh/quadtree.hpp
                                    src/metacity/geometry/mesh/quadtree.cpp
                                    src/metacity/geometry/mesh/triangulation.hpp
                                    src/metacity/geometry/mesh/triangulation.cpp)

install(TARGETS geometry DESTINATION .)
