#!/bin/bash

# Get script directory (without using /usr/bin/realpath)
CI_DIR=$(cd `dirname "${BASH_SOURCE[0]}"` && pwd)
# Install/update uv
$CI_DIR/install-tools.sh

# Python information (platform and version)
if ! [ -z "$UV_PYTHON" ]; then
    PYTHON=$(uv python find $UV_PYTHON)
elif which python &>/dev/null; then
    PYTHON=python
else
    exit 1
fi
PY_PLATFORM=$($PYTHON -c "import sysconfig; print(sysconfig.get_platform(), end='')")
PY_VERSION=$($PYTHON -c "import sysconfig; print(sysconfig.get_python_version(), end='')")
PY_VERSION_FULL=$($PYTHON -c "import sysconfig; print(sysconfig.get_config_var('py_version'), end='')")
PY_VERSION_NODOT=$($PYTHON -c "import sysconfig; print(sysconfig.get_config_var('py_version_nodot'), end='')")
PY_ABI_THREAD=$($PYTHON -c "import sysconfig; print(sysconfig.get_config_var('abi_thread') or '', end='')")

PYTHON_TAG=cp$PY_VERSION_NODOT
if [[ $PY_PLATFORM == linux* ]]; then
    PLATFORM_TAG=many$(echo $PY_PLATFORM | sed 's/\-/_/')
    PLATFORM_TAG_MASK="$(echo $PLATFORM_TAG | sed 's/_/*_/')"
    if ! [ "$CI" == "true" ] && which podman >/dev/null; then
        export CIBW_CONTAINER_ENGINE=podman
    fi
elif [[ $PY_PLATFORM == macosx* ]]; then
    PLATFORM_TAG=macosx_universal2
    PLATFORM_TAG_MASK="macosx_*"
else
    PLATFORM_TAG=$(echo $PY_PLATFORM | sed 's/\-/_/')
    PLATFORM_TAG_MASK="win*"
fi
BUILD_TAG_DEFAULT="$PYTHON_TAG-$PLATFORM_TAG$PY_ABI_THREAD"

# Usage
if ! [ -z "$1" ] && [ "$1" == "--help" ]; then
    echo "Usage:"
    echo "$0 [--all|TAG] [--archs=ARCHS]"
    echo "Where:"
    echo "  --all     Build all valid wheels for current OS."
    echo "  TAG       Force build the wheel for the given identifier."
    echo "            [default: $BUILD_TAG_DEFAULT]"
    echo "  --install Install after build."
    exit 1
fi

BUILD_TAG="$BUILD_TAG_DEFAULT"
INSTALL=""
while ! [ -z "$1" ]; do
    if [ "$1" == "--all" ]; then
        BUILD_TAG=""
    elif [ "$1" == "--install" ]; then
        INSTALL=true
    else
        BUILD_TAG="$1"
    fi
    shift
done

# Use of dev tools
_bump_my_version () {
    local args=$*
    local value=$($HOME/bin/bump-my-version $args 2>/dev/null)
    echo $($PYTHON -c "print('$value'.replace('\r','').replace('\n',''), end='')")
}

_build_wheel () {
    local args=$*

    if [[ $PY_PLATFORM == mingw* ]]; then
        $PYTHON -m build -n -x --wheel -o wheelhouse
    elif [[ $PY_PLATFORM == win* ]] && [[ $args == *--only* ]]; then
        uv build -p $PY_VERSION$PY_ABI_THREAD --wheel -o wheelhouse
    else
        # Do not export UV_SYSTEM_PYTHON to avoid conflict with uv in
        # cibuildwheel on macOS and Windows
        unset UV_SYSTEM_PYTHON
        $HOME/bin/cibuildwheel $args
    fi
}

echo "::group::Detect version"
VERSION=$(_bump_my_version show current_version)
if [ -z $VERSION ]; then
    VERSION=$(grep "__version__ = " cx_Freeze/__init__.py | sed 's/-/./' | awk -F\" '{print $2}')
fi
if [[ $VERSION == *-* ]]; then
    VERSION_OK=$($PYTHON -c "print(''.join('$VERSION'.replace('-','.').rsplit('.',1)), end='')")
else
    VERSION_OK=$VERSION
fi
echo "::endgroup::"

mkdir -p wheelhouse >/dev/null
if [[ $PY_PLATFORM == linux* ]]; then
    FILEMASK="cx_freeze-$VERSION_OK.tar.gz"
    if [ -z $(ls "wheelhouse/$FILEMASK" 2>/dev/null || echo '') ]; then
        echo "::group::Build sdist"
        uv build -p $PY_VERSION$PY_ABI_THREAD --sdist -o wheelhouse
        echo "::endgroup::"
    fi
fi
echo "::group::Build wheel(s)"
if [ "$BUILD_TAG" == "$BUILD_TAG_DEFAULT" ]; then
    DIRTY=$(_bump_my_version show scm_info.dirty)
    FILEMASK="cx_Freeze-$VERSION_OK-$PYTHON_TAG-$PYTHON_TAG$PY_ABI_THREAD-$PLATFORM_TAG_MASK"
    FILEEXISTS=$(ls wheelhouse/$FILEMASK.whl 2>/dev/null || echo '')
    if [ "$DIRTY" != "False" ] || [ -z "$FILEEXISTS" ]; then
        _build_wheel --only "$BUILD_TAG_DEFAULT"
    fi
elif ! [ -z "$BUILD_TAG" ]; then
    CIBW_BUILD="$BUILD_TAG" _build_wheel
else
    _build_wheel
fi
echo "::endgroup::"

if [ "$INSTALL" == "true" ] || ! [ "$CI" == "true" ]; then
    echo "::group::Install cx_Freeze $VERSION_OK"
    if [[ $PY_PLATFORM == mingw* ]]; then
        pip install "cx_Freeze==$VERSION_OK" -f wheelhouse \
            --no-deps --no-index --force-reinstall
    else
        uv pip install "cx_Freeze==$VERSION_OK" -f wheelhouse \
            --no-build --no-deps --no-index --prerelease=allow --reinstall
    fi
    echo "::endgroup::"
fi
