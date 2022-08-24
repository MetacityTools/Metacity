#!/bin/bash

git checkout release
if [ $? -ne 0 ]; then
    echo "Failed to checkout release"
    exit 1
fi

echo "Checking version of Metacity 🏙"
echo "--------------------------------"
GIT_VERSION=$(git describe --tags --abbrev=0 2>/dev/null)
if [ -z "$GIT_VERSION" ]; then
    GIT_VERSION="None"
fi
CURRENT_VERSION=$(python3 setup.py --version) 
echo "The latest version on github is $GIT_VERSION, the current local version is $CURRENT_VERSION"

git checkout dev
if [ $? -ne 0 ]; then
    echo "Failed to checkout dev"
    exit 1
fi

echo "Done."
echo "Note: You are now on the dev branch"

