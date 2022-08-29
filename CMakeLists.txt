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


pybind11_add_module(geometry        src/cpp/geometry.cpp 
                                    src/cpp/types.hpp
                                    src/cpp/convert.hpp
                                    src/cpp/progress.hpp 
                                    src/cpp/mesh_pipeline/bbox.hpp 
                                    src/cpp/mesh_pipeline/bbox.cpp 
                                    src/cpp/mesh_pipeline/modifiers.hpp 
                                    src/cpp/mesh_pipeline/modifiers.cpp 
                                    src/cpp/mesh_pipeline/graham.hpp 
                                    src/cpp/mesh_pipeline/graham.cpp 
                                    src/cpp/mesh_pipeline/bvh.hpp 
                                    src/cpp/mesh_pipeline/bvh.cpp 
                                    src/cpp/mesh_pipeline/model.hpp 
                                    src/cpp/mesh_pipeline/model.cpp 
                                    src/cpp/mesh_pipeline/layer.hpp 
                                    src/cpp/mesh_pipeline/layer.cpp 
                                    src/cpp/mesh_pipeline/attribute.hpp 
                                    src/cpp/mesh_pipeline/attribute.cpp 
                                    src/cpp/mesh_pipeline/grid.hpp
                                    src/cpp/mesh_pipeline/grid.cpp
                                    src/cpp/mesh_pipeline/triangulation.hpp
                                    src/cpp/mesh_pipeline/triangulation.cpp
                                    src/cpp/vector_pipeline/graph.hpp
                                    src/cpp/vector_pipeline/graph.cpp)

install(TARGETS geometry DESTINATION .)
