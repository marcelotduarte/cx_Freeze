#!/bin/bash

# Get script directory (without using /usr/bin/realpath)
_CI_DIR=$(dirname "${BASH_SOURCE[0]}")
CI_DIR=$(cd "$_CI_DIR" && pwd)

# Python information (platform and version)
INSTALL_TOOLS="1"
if [ -n "$UV_PYTHON" ]; then
    if ! which uv &>/dev/null; then
        # Install/update uv
        "$CI_DIR/install-tools.sh"
        INSTALL_TOOLS="0"
    fi
    PYTHON=$(uv python find "$UV_PYTHON")
elif which python &>/dev/null; then
    PYTHON=python
else
    exit 1
fi
PY_PLATFORM=$($PYTHON -c "import sysconfig; print(sysconfig.get_platform(), end='')")
PY_VERSION=$($PYTHON -c "import sysconfig; print(sysconfig.get_python_version(), end='')")
PY_ABI_THREAD=$($PYTHON -c "import sysconfig; print(sysconfig.get_config_var('abi_thread') or '', end='')")

IS_CONDA=$([ -n "$CONDA_EXE" ] && echo "1")
IS_MINGW=$([[ $PY_PLATFORM == mingw* ]] && echo "1")

# Usage
if [ -n "$1" ] && [ "$1" == "--help" ]; then
    echo "Usage:"
    echo "$0 [--install]"
    echo "Where:"
    echo "  --install Install after build [default on local builds]."
    exit 1
fi

BUILD_TAG=py3-none-any
if [ "$CI" == "true" ]; then
    INSTALL="0"
else
    INSTALL="1"
fi
while [ -n "$1" ]; do
    if [ "$1" == "--install" ]; then
        INSTALL="1"
    fi
    shift
done

# Install/update uv and dev tools
INSTALL_DEV="0"
if [ "$IS_CONDA" == "1" ] || [ "$IS_MINGW" == "1" ]; then
    if ! [ -e "$HOME/bin/bump-my-version" ]; then
        INSTALL_DEV="1"
    fi
else
    if [[ $PY_PLATFORM == linux* ]]; then
        if ! [ -e "$HOME/bin/bump-my-version" ]; then
            INSTALL_DEV="1"
        fi
    else
        if ! which bump-my-version &>/dev/null || \
           ! which pyproject-build &>/dev/null; then
            INSTALL_DEV="1"
        fi
    fi
fi

if [ "$INSTALL_TOOLS" == "1" ] || [ "$INSTALL_DEV" == "1" ]; then
    if [ "$INSTALL_DEV" == "1" ]; then
        "$CI_DIR/install-tools.sh" --dev
    else
        "$CI_DIR/install-tools.sh"
    fi
fi

# Use of dev tools
_bump_my_version () {
    local value
    if which bump-my-version &>/dev/null; then
        value=$(bump-my-version "$*" 2>/dev/null)
    elif [ -e "$HOME/bin/bump-my-version" ]; then
        value=$("$HOME/bin/bump-my-version" "$*" 2>/dev/null)
    else
        exit 1
    fi
    $PYTHON -c "print('$value'.replace('\r','').replace('\n',''), end='')"
}

_build_sdist () {
    if [ "$IS_CONDA" == "1" ] || [ "$IS_MINGW" == "1" ]; then
        $PYTHON -m build -n -x --sdist -o wheelhouse
    elif which pyproject-build &>/dev/null; then
         $PYTHON -m build --sdist -o wheelhouse
    else
        uv build -p "$PY_VERSION$PY_ABI_THREAD" --sdist -o wheelhouse
    fi
}

_build_wheel () {
    if [ "$IS_CONDA" == "1" ] || [ "$IS_MINGW" == "1" ]; then
        $PYTHON -m build -n -x --wheel -o wheelhouse
    elif which pyproject-build &>/dev/null; then
         $PYTHON -m build --wheel -o wheelhouse
    else
        uv build -p "$PY_VERSION$PY_ABI_THREAD" --wheel -o wheelhouse
    fi
}

echo "::group::Project version"
NAME=$(grep -m1 "^name = " pyproject.toml | awk -F\" '{print $2}')
NORMALIZED_NAME=$(echo "$NAME" | tr '[:upper:]' '[:lower:]' | tr '-' '_')
VERSION=$(_bump_my_version show current_version)
if [ -z "$VERSION" ]; then
    if [ -d src ]; then
        FILENAME=src/$NORMALIZED_NAME/__init__.py
    else
        FILENAME=$NAME/__init__.py
    fi
    VERSION=$(grep "__version__ = " "${FILENAME/-/.}" | awk -F\" '{print $2}')
fi
if [[ $VERSION == *-* ]]; then
    NORMALIZED_VERSION=$($PYTHON -c "print(''.join('$VERSION'.replace('-','.').rsplit('.',1)), end='')")
else
    NORMALIZED_VERSION=$VERSION
fi
echo "Name: $NAME ($NORMALIZED_NAME)"
echo "Version: $VERSION ($NORMALIZED_VERSION)"
echo "::endgroup::"

mkdir -p wheelhouse >/dev/null
DIRTY=$(_bump_my_version show scm_info.dirty)
FILEMASK="$NORMALIZED_NAME-$NORMALIZED_VERSION"
FILEEXISTS=$(find "wheelhouse/$FILEMASK.tar.gz" 2>/dev/null || echo '')
if [ "$DIRTY" == "True" ] || [ -z "$FILEEXISTS" ]; then
    echo "::group::Build sdist"
    _build_sdist
    echo "::endgroup::"
fi
echo "::group::Build wheel(s)"
FILEMASK="$NORMALIZED_NAME-$NORMALIZED_VERSION-$BUILD_TAG"
FILEEXISTS=$(find "wheelhouse/$FILEMASK.whl" 2>/dev/null || echo '')
if [ "$DIRTY" == "True" ] || [ -z "$FILEEXISTS" ]; then
    _build_wheel
fi
echo "::endgroup::"

if [ "$INSTALL" == "1" ]; then
    echo "::group::Install $NORMALIZED_NAME $NORMALIZED_VERSION"
    if [[ $PY_PLATFORM == mingw* ]]; then
        PIP_COMMAND="pip install --force-reinstall"
    else
        PIP_COMMAND="uv pip install --no-build --prerelease=allow --reinstall"
    fi
    $PIP_COMMAND "$NORMALIZED_NAME==$NORMALIZED_VERSION" -f wheelhouse \
        --no-deps --no-index
    echo "::endgroup::"
fi
