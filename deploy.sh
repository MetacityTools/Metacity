#!/bin/bash

#python setup.py sdist bdist_wheel; \
#rm dist/metacity*; \
python setup.py sdist; \
python -m twine upload dist/*;
