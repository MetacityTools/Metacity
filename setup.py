import pathlib
from setuptools import setup, find_packages, Extension
import pybind11
from typing import List

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()


# generate an Extension object from its dotted name
def makeExtension(module: str, path: str, cfiles: List[str]):
    cpppaths = [ str(HERE / "metacity" / path / f) + '.cpp' for f in cfiles ]     
    return Extension(
        module,
        cpppaths,
        extra_compile_args=["-Wall", "-pedantic", "-std=c++17", "-g", "-fsanitize=address", "-fno-omit-frame-pointer", "-shared-libasan"],
        extra_link_args=["-fsanitize=address", "-shared-libasan"],#, '-ffast-math', '-O2'],
        include_dirs = [pybind11.get_include()],
        language='c++',
        undef_macros=[ "NDEBUG" ]
        )

dfiles = ["primitive", "primitives", "points", "lines", "polygons", "triangulation", "slicing"]
extension = [makeExtension("metacity.geometry.primitive", "geometry", dfiles)]

# This call to setup() does all the work
setup(
    name="metacity",
    packages = find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    ext_modules=extension,
    version="0.0.32",
    description="Python toolkit for Urban Data processing",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/MetacitySuite/Metacity",
    author="Metacity",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires='>=3.8', 
    setup_requires=['pybind11>=2.5.0'],    
    install_requires = [
        "dotmap>=1.3.23",
        "earcut>=1.1.4",
        "numpy>=1.21.1",
        "tqdm>=4.62.0",
        "geopandas>=0.9.0",
        "pybind11>=2.7.0",
        "setuptools>=42",
        "wheel",
    ]
)