#!/bin/bash

if [ -z "${VIRTUAL_ENV}" ] && [ -z "${CI}" ] ; then
	echo "Required: use of a virtual environment or CI."
    exit 1
fi


echo "::group::Prepare the environment"
if [ -z "${POLICY}" ] ; then
    POLICY=manylinux2014
fi
if [ -z "${PLATFORM}" ] ; then
    PLATFORM=x86_64
fi
if [ -z "${COMMIT_SHA}" ] ; then
    COMMIT_SHA=latest
fi

# Get script directory
CI_DIR=$(dirname "${BASH_SOURCE[0]}")
pushd ${CI_DIR}/.. >/dev/null
TOP_DIR=$(pwd)
popd >/dev/null
echo "::endgroup::"

echo "::group::Build the wheels"
pushd $TOP_DIR >/dev/null

CIBW_MANYLINUX_X86_64_IMAGE="quay.io/pypa/${POLICY}_x86_64:${COMMIT_SHA}" \
    CIBW_PRERELEASE_PYTHONS=true cibuildwheel --platform linux --archs $PLATFORM

popd >/dev/null
echo "::endgroup::"
