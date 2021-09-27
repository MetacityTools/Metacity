import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="metacity",
    packages = find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    version="0.0.18",
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
    python_requires='>=3.8',                # Minimum version requirement of the package
    install_requires = [
        "dotmap>=1.3.23",
        "earcut>=1.1.4",
        "numpy>=1.21.1",
        "tqdm>=4.62.0",
        "geopandas>=0.9.0"
    ]
)