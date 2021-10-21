#!/bin/bash

#python setup.py sdist bdist_wheel; \
#rm dist/metacity*; \
rm -rf dist;
rm -rf metacity.egg*;
python setup.py sdist; 
python -m twine upload dist/*;
