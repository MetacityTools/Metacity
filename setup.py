from importlib.metadata import requires
import sys

try:
    from skbuild import setup
except ImportError:
    print(
        "Please update pip, you need pip 10 or greater,\n"
        " or you need to install the PEP 518 requirements in pyproject.toml yourself",
        file=sys.stderr,
    )
    raise

from setuptools import find_packages
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent
# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="metacity",
    version="0.6.0",
    author="Vojtěch Tomas",
    author_email="hello@vojtatom.cz",
    license="MIT",
    description="Python toolkit for Urban Data processing",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    cmake_install_dir="src/metacity",
    install_requires = [
        "orjson>=3.6.4",
        "colored>=1.4.3",
        "six",
        "protobuf>=4.21.7"
    ],
    url="https://github.com/MetacitySuite/Metacity",
    python_requires='>=3.8',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ]
)
