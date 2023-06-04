#!/bin/bash

if [ -z "${VIRTUAL_ENV}" ] && [ -z "${CI}" ] ; then
	echo "Required: use of a virtual environment or CI."
    exit 1
fi

echo "::group::Prepare the environment"
if [ -z "${POLICY}" ] ; then
    export POLICY=manylinux2014
fi
if [ -z "${PLATFORM}" ] ; then
    export PLATFORM=x86_64
fi
if [ -z "${COMMIT_SHA}" ] ; then
    export COMMIT_SHA=latest
fi
docker buildx version
docker buildx create --name builder-manylinux --driver docker-container --use
docker buildx inspect --bootstrap --builder builder-manylinux

# Get script directory
CI_DIR=$(dirname "${BASH_SOURCE[0]}")
pushd "$CI_DIR/.." >/dev/null
TOP_DIR=$(pwd)
popd >/dev/null

# Set manylinux as working directory
ML_DIR="$TOP_DIR/../manylinux"
if ! [ -d "$ML_DIR" ] ; then
    git clone -v https://github.com/marcelotduarte/manylinux.git "$ML_DIR"
fi
echo "::endgroup::"

echo "::group::Build"
pushd "$ML_DIR" >/dev/null
git checkout main
./build.sh
popd >/dev/null
echo "::endgroup::"
