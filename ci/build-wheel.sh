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
PY_VERSION_NODOT=$($PYTHON -c "import sysconfig; print(sysconfig.get_config_var('py_version_nodot'), end='')")
PY_ABI_THREAD=$($PYTHON -c "import sysconfig; print(sysconfig.get_config_var('abi_thread') or '', end='')")

IS_CONDA=$([ -n "$CONDA_EXE" ] && echo "1")
IS_MINGW=$([[ $PY_PLATFORM == mingw* ]] && echo "1")

PYTHON_TAG=cp$PY_VERSION_NODOT
if [ "$IS_CONDA" == "1" ]; then
    PLATFORM_TAG=${PY_PLATFORM/-/_}
    PLATFORM_TAG_MASK=$PLATFORM_TAG
else
    if [[ $PY_PLATFORM == linux* ]]; then
        PLATFORM_TAG=many${PY_PLATFORM/-/_}
        PLATFORM_TAG_MASK=${PLATFORM_TAG/_/*_}
        if ! [ "$CI" == "true" ] && which podman &>/dev/null; then
            export CIBW_CONTAINER_ENGINE=podman
        fi
    elif [[ $PY_PLATFORM == macosx* ]]; then
        PLATFORM_TAG=macosx_universal2
        PLATFORM_TAG_MASK="macosx_*"
    else
        PLATFORM_TAG=${PY_PLATFORM/-/_}
        PLATFORM_TAG_MASK="win*"
    fi
fi
BUILD_TAG_DEFAULT="$PYTHON_TAG$PY_ABI_THREAD-$PLATFORM_TAG"

# Usage
if [ -n "$1" ] && [ "$1" == "--help" ]; then
    echo "Usage:"
    echo "$0 [--all|TAG] [--install]"
    echo "Where:"
    echo "  --all     Build all valid wheels for current OS."
    echo "  TAG       Force build the wheel for the given identifier."
    echo "            [default: $BUILD_TAG_DEFAULT]"
    echo "  --install Install after build [default on local builds]."
    exit 1
fi

BUILD_TAG="$BUILD_TAG_DEFAULT"
if [ "$CI" == "true" ]; then
    INSTALL="0"
else
    INSTALL="1"
fi
while [ -n "$1" ]; do
    if [ "$1" == "--all" ]; then
        BUILD_TAG=""
    elif [ "$1" == "--install" ]; then
        INSTALL="1"
    else
        BUILD_TAG="$1"
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
        if ! [ -e "$HOME/bin/bump-my-version" ] || \
           ! [ -e "$HOME/bin/cibuildwheel" ]; then
            INSTALL_DEV="1"
        fi
    else
        if ! which bump-my-version &>/dev/null || \
           ! which cibuildwheel &>/dev/null || \
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
    elif [ -e "$HOME/bin/pyproject-build" ]; then
        "$HOME/bin/pyproject-build" --sdist -o wheelhouse
    elif which pyproject-build &>/dev/null; then
         $PYTHON -m build --sdist -o wheelhouse
    else
        uv build -p "$PY_VERSION$PY_ABI_THREAD" --sdist -o wheelhouse
    fi
}

_build_wheel () {
    local args=$*
    if [ "$IS_CONDA" == "1" ] || [ "$IS_MINGW" == "1" ]; then
        $PYTHON -m build -n -x --wheel -o wheelhouse
    elif [[ $PY_PLATFORM == win* ]] && [[ $args == *--only* ]]; then
        uv build -p "$PY_VERSION$PY_ABI_THREAD" --wheel -o wheelhouse
    elif [[ $PY_PLATFORM == macos* ]] && [[ $args == *--only* ]]; then
        uv build -p "$PY_VERSION$PY_ABI_THREAD" --wheel -o wheelhouse
    else
        # Do not export UV_SYSTEM_PYTHON to avoid conflict with uv in
        # cibuildwheel on macOS and Windows
        unset UV_SYSTEM_PYTHON
        if [ -e "$HOME/bin/cibuildwheel" ]; then
            "$HOME/bin/cibuildwheel" "$args"
        else
            $PYTHON -m cibuildwheel "$args"
        fi
    fi
}

echo "::group::Project version"
NAME=$(grep "^name = " pyproject.toml | awk -F\" '{print $2}')
NORMALIZED_NAME=$(echo "$NAME" | tr '[:upper:]' '[:lower:]')
VERSION=$(_bump_my_version show current_version)
if [ -z "$VERSION" ]; then
    if [ -d src ]; then
        FILENAME=src/$NAME/__init__.py
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
FILEEXISTS=$(ls "wheelhouse/$FILEMASK.tar.gz" 2>/dev/null || echo '')
if [ "$DIRTY" == "True" ] || [ -z "$FILEEXISTS" ]; then
    echo "::group::Build sdist"
    _build_sdist
    echo "::endgroup::"
fi
echo "::group::Build wheel(s)"
if [ "$BUILD_TAG" == "$BUILD_TAG_DEFAULT" ]; then
    FILEMASK="$NORMALIZED_NAME-$NORMALIZED_VERSION-$PYTHON_TAG-$PYTHON_TAG$PY_ABI_THREAD-$PLATFORM_TAG_MASK"
    FILEEXISTS=$(ls "wheelhouse/$FILEMASK.whl" 2>/dev/null || echo '')
    if [ "$DIRTY" == "True" ] || [ -z "$FILEEXISTS" ]; then
        _build_wheel --only "$BUILD_TAG_DEFAULT"
    fi
elif [ -n "$BUILD_TAG" ]; then
    CIBW_BUILD="$BUILD_TAG" _build_wheel
else
    _build_wheel
fi
echo "::endgroup::"

if [ "$INSTALL" == "1" ]; then
    echo "::group::Install $NORMALIZED_NAME $NORMALIZED_VERSION"
    if [[ $PY_PLATFORM == mingw* ]]; then
        pip install "$NORMALIZED_NAME==$NORMALIZED_VERSION" -f wheelhouse \
            --no-deps --no-index --force-reinstall
    else
        uv pip install "$NORMALIZED_NAME==$NORMALIZED_VERSION" -f wheelhouse \
            --no-build --no-deps --no-index --prerelease=allow --reinstall
    fi
    echo "::endgroup::"
fi
