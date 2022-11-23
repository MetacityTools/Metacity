#!/bin/bash

git checkout release 1>/dev/null 2>/dev/null
git pull 1>/dev/null 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Failed to checkout release"
    exit 1
fi

GIT_VERSION=$(git describe --tags --abbrev=0 2>/dev/null)
if [ -z "$GIT_VERSION" ]; then
    GIT_VERSION="None"
fi
CURRENT_VERSION=$(python3 setup.py --version) 
echo "The latest versions:"
echo "    github (release):  $GIT_VERSION"
echo "               local:  $CURRENT_VERSION"

git checkout dev 1>/dev/null 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Failed to checkout dev"
    exit 1
fi

echo "Note: You are now on the dev branch"

