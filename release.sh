#!/bin/bash
echo "Releasing new version of BananaGL 🍌"
echo "--------------------------------"
GIT_VERSION=$(git describe --tags --abbrev=0 2>/dev/null)
if [ -z "$GIT_VERSION" ]; then
    GIT_VERSION="None"
fi
CURRENT_VERSION=$(python3 setup.py --version) 
echo "The latest version on github is $GIT_VERSION, the current local version is $CURRENT_VERSION"
echo "Please specify new version number (e.g. $CURRENT_VERSION - without \"v\"):"
while read version; do
    version_checked=$(echo $version | sed -e '/^[0-9]*\.[0-9]*\.[0-9]*$/d')
    if [[ -z $version_checked ]]; then
        echo "Releasing version $version..."
        break
    else
        echo "$version_checked is not in the right format, please use XX.XX.XX format (ie: 4.15.3)"
    fi
done

VERSION=$version
TAG_VERSION="v$VERSION"

exit 1
git checkout main
if [ $? -ne 0 ]; then
    echo "Failed to checkout main"
    exit 1
fi
git pull
if [ $? -ne 0 ]; then
    echo "Failed to pull main"
    exit 1
fi

sed -i '' "s/${CURRENT_VERSION}/${VERSION}/" setup.py

git add setup.py
if [ $? -ne 0 ]; then
    echo "Failed to add setup.py"
    exit 1
fi
git commit -m "Release ${TAG_VERSION}"
if [ $? -ne 0 ]; then
    echo "Failed to commit setup.py"
    exit 1
fi
git push origin main
if [ $? -ne 0 ]; then
    echo "Failed to push setup.py"
    exit 1
fi
git tag $TAG_VERSION
if [ $? -ne 0 ]; then
    echo "Failed to tag main"
    exit 1
fi
git push origin --tags
if [ $? -ne 0 ]; then
    echo "Failed to push tags"
    exit 1
fi

rm -rf dist;
rm -rf metacity.egg*;
python setup.py sdist; 
python -m twine upload dist/*;

git checkout dev
if [ $? -ne 0 ]; then
    echo "Failed to checkout dev"
    exit 1
fi

echo "Done."
echo "Note: You are now on the dev branch"

