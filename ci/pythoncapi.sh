#!/bin/bash

# Get script directory (without using /usr/bin/realpath)
_CI_DIR=$(dirname "${BASH_SOURCE[0]}")
CI_DIR=$(cd "$_CI_DIR" && pwd)
TOP_DIR=$(cd "$CI_DIR"/.. && pwd)

CI_TMPDIR=$(python -c "import tempfile; print(tempfile.mkdtemp())")
pushd "$CI_TMPDIR" >/dev/null || exit
git clone -q https://github.com/python/pythoncapi-compat
popd >/dev/null || exit
pushd "$CI_TMPDIR"/pythoncapi-compat >/dev/null || exit
python upgrade_pythoncapi.py --download "$TOP_DIR"/source/bases/
cp "$TOP_DIR"/source/bases/pythoncapi_compat.h "$TOP_DIR"/source/legacy/
python upgrade_pythoncapi.py "$TOP_DIR"/source/
popd >/dev/null || exit
