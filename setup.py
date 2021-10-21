import pathlib
from setuptools import setup, find_packages, Extension
from setuptools.command.build_ext import build_ext

import os
import subprocess

from setuptools import setup, Extension
from setuptools import find_packages
from setuptools.command.build_ext import build_ext

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()


class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=''):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    def run(self):
        try:
            _ = subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError("CMake must be installed to build the following extensions: " +
                               ", ".join(e.name for e in self.extensions))

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        # required for auto-detection of auxiliary "native" libs
        if not extdir.endswith(os.path.sep):
            extdir += os.path.sep

        #cmake_args = ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + extdir,
        #              '-DPYTHON_EXECUTABLE=' + sys.executable]

        cfg = 'Debug' if self.debug else 'Release'
        build_args = ['--config', cfg]

        cmake_args = ['-DCMAKE_BUILD_TYPE=' + cfg]
        build_args += ['--', '-j2']

        env = os.environ.copy()
        env['CXXFLAGS'] = '{} -DVERSION_INFO=\\"{}\\"'.format(env.get('CXXFLAGS', ''),
                                                              self.distribution.get_version())
        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)
        subprocess.check_call(['cmake', ext.sourcedir] + cmake_args, cwd=self.build_temp, env=env)
        subprocess.check_call(['cmake', '--build', '.'] + build_args, cwd=self.build_temp)


# This call to setup() does all the work
setup(
    name="metacity",
    packages = find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    ext_modules=[CMakeExtension('metacity.geometry.primitive')],
    cmdclass=dict(build_ext=CMakeBuild),
    version="0.0.34",
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