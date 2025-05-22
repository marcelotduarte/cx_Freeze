#!/bin/bash

# Get script directory (without using /usr/bin/realpath)
CI_DIR=$(cd `dirname "${BASH_SOURCE[0]}"` && pwd)
TOP_DIR=$(cd $CI_DIR/.. && pwd)

CI_TMPDIR=$(python -c "import tempfile; print(tempfile.mkdtemp())")
pushd $CI_TMPDIR >/dev/null
git clone -q https://github.com/python/pythoncapi-compat
if [ -d pythoncapi-compat ]; then
    cd pythoncapi-compat
    python upgrade_pythoncapi.py --download $TOP_DIR/source/bases/
    cp $TOP_DIR/source/bases/pythoncapi_compat.h $TOP_DIR/source/legacy/
    python upgrade_pythoncapi.py $TOP_DIR/source/
fi
popd >/dev/null
