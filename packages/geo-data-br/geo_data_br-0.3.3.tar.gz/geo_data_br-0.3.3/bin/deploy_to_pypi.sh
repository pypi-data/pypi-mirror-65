#!/bin/bash
cd $(git rev-parse --show-toplevel)
set -e

BUILD=1 ./bin/test.sh

rm -rf dist build *.egg-info
python setup.py sdist bdist_wheel
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
echo 'to prod? (press enter)'; read;
twine upload dist/*
git push --tags
