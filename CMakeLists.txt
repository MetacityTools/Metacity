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
                                    src/metacity/geometry/mesh_pipeline/bbox.hpp 
                                    src/metacity/geometry/mesh_pipeline/bbox.cpp 
                                    src/metacity/geometry/mesh_pipeline/modifiers.hpp 
                                    src/metacity/geometry/mesh_pipeline/modifiers.cpp 
                                    src/metacity/geometry/mesh_pipeline/graham.hpp 
                                    src/metacity/geometry/mesh_pipeline/graham.cpp 
                                    src/metacity/geometry/mesh_pipeline/bvh.hpp 
                                    src/metacity/geometry/mesh_pipeline/bvh.cpp 
                                    src/metacity/geometry/mesh_pipeline/model.hpp 
                                    src/metacity/geometry/mesh_pipeline/model.cpp 
                                    src/metacity/geometry/mesh_pipeline/layer.hpp 
                                    src/metacity/geometry/mesh_pipeline/layer.cpp 
                                    src/metacity/geometry/mesh_pipeline/attribute.hpp 
                                    src/metacity/geometry/mesh_pipeline/attribute.cpp 
                                    src/metacity/geometry/mesh_pipeline/grid.hpp
                                    src/metacity/geometry/mesh_pipeline/grid.cpp
                                    src/metacity/geometry/mesh_pipeline/triangulation.hpp
                                    src/metacity/geometry/mesh_pipeline/triangulation.cpp
                                    src/metacity/geometry/vector_pipeline/graph.hpp
                                    src/metacity/geometry/vector_pipeline/graph.cpp)

install(TARGETS geometry DESTINATION .)
