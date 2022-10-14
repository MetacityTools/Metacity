from .encode import Encoder
from .decode import Decoder

__version__ = '2.0.0'



# Original source: https://github.com/pygeobuf/pygeobuf
# ISC License
# Copyright (c) 2014, Mapbox
# Included in Metacity directly, not as a dependency, 
# since the pypi package is not up to date.



def encode(*args):
    return Encoder().encode(*args)


def decode(*args):
    return Decoder().decode(*args)
