# Metacity

[![Build Status](https://github.com/MetacitySuite/Metacity/workflows/Metacity%20CI/badge.svg)](https://github.com/MetacitySuite/Metacity/actions?query=workflow%3A%22Metacity+CI%22)
[![Coverage Status](https://coveralls.io/repos/github/MetacitySuite/Metacity/badge.svg?branch=main)](https://coveralls.io/github/MetacitySuite/Metacity?branch=main)
[![Pypi version](https://badge.fury.io/py/metacity.svg)](https://pypi.org/project/metacity/)

Toolkit for Urban Data Processing

## Installation

Install with:
```
pip install metacity
```

This repository relies on system packages `GDAL` and `CMake`, please make sure they are installed before trying to install this package. On Ubuntu, you can try something like:

1. Install [GDAL](https://mothergeo-py.readthedocs.io/en/latest/development/how-to/gdal-ubuntu-pkg.html)
```
sudo add-apt-repository ppa:ubuntugis/ppa
sudo apt-get update
sudo apt-get install gdal-bin
sudo apt-get install libgdal-dev
export CPLUS_INCLUDE_PATH=/usr/include/gdal
export C_INCLUDE_PATH=/usr/include/gdal
```
2. Install [CMake](https://cmake.org/download/)
```
sudo apt-get install cmake
```

## Development
1. Clone this repository:
```
git clone git@github.com:MetacitySuite/Metacity.git
```
2. Initialize submodules:
```
git submodule update --init --recursive
```
3. Install requirements:
```
pip install -r requirements.txt
```
4. Build C++ with:
```
python setup.py build_ext --inplace
```
If you encounter any problems, make sure you installed dependencies listed above, generally:
- have `GDAL` and `CMake` installed
- install packages based on `requirements.txt`
- make sure you have c++ compiler supporting c++17 installed

## Branches
| Branch | Status | Description |
| ------ | ------ | ----------- |
| main   | [![Build Status](https://github.com/MetacitySuite/Metacity/workflows/Metacity%20CI/badge.svg?branch=main)](https://github.com/MetacitySuite/Metacity/actions?query=workflow%3A%22Metacity+CI%22) | protected, merged PRs auto tested and deployed to PyPI |
| dev    | [![Build Status](https://github.com/MetacitySuite/Metacity/workflows/Metacity%20CI/badge.svg?branch=dev)](https://github.com/MetacitySuite/Metacity/actions?query=workflow%3A%22Metacity+CI%22) | merged PRs auto tested and version bumped if tag present |


## PR Merge Commit message conventions
Use any of the following tags in the merge commit message title to indicate the type of PR:

| In commit message | Descrition | Branches |
| ---------------------- | ----------- | ------- |
| `action::bump` | flag to run bump package version | dev |
| `action::package` | flag to run deploy to PyPI | main |

Dev branch actions (together with `action::bump`):

| In commit message | Descrition | Branches |
| ---------------------- | ----------- | ------- |
| `version::patch` | bump version after patch/bug fix/minor change | dev |
| `version::minor` | bump version after new feature/minor change | dev |
| `version::major` | bump version after major change/breaking change | dev |

If no tag is used, no action runs after the PR is merged. If no version tag is used, the version is bumped as patch.


