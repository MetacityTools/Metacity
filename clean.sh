#!/bin/bash

find . -type d -not -path "*/env/*" -wholename '*/build' -exec rm -r {} +;\
find . -type f -not -path "*/env/*" -name '*.so' -exec rm {} +;\