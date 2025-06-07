#!/bin/bash

# Get script directory
THIS_DIR=$(dirname "${BASH_SOURCE[0]}")

pushd "$THIS_DIR" >/dev/null || exit
pyside6-rcc -o _resource.py resource.qrc
popd >/dev/null || exit
