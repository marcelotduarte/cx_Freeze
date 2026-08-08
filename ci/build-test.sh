#!/bin/bash

# Verify if python is installed
PYTHON=""
if which python &>/dev/null; then
    if [[ $(python -V) == *3.* ]]; then
        PYTHON=$(which python)
    fi
fi
if [ -z "$PYTHON" ] && which python3 &>/dev/null; then
    PYTHON=python3
fi
if [ -z "$PYTHON" ]; then
    echo "ERROR: python3 not found"
    exit 1
fi

# Get script directory
CI_DIR=$(dirname "${BASH_SOURCE[0]}")

if [ "$OSTYPE" == "cygwin" ] || [ "$OSTYPE" == "msys" ]; then
    PLATFORM=windows
else
    PLATFORM=linux
fi

for sample in $($PYTHON ci/_platform.py $PLATFORM --plain); do
    "$CI_DIR/build-test-one.sh" "$sample" --venv --deps=d
    TEST_EXITCODE=$?
    if ! [ "$TEST_EXITCODE" == "0" ]; then
        echo "ABORTING..."
        exit $TEST_EXITCODE
    fi
done
