#!/bin/bash

# Python information (platform and version)
PYTHON=python
PY_PLATFORM=$($PYTHON -c "import sysconfig; print(sysconfig.get_platform(), end='')")
PY_VERSION=$($PYTHON -c "import sysconfig; print(sysconfig.get_python_version(), end='')")
PY_VERSION_FULL=$($PYTHON -c "import sysconfig; print(sysconfig.get_config_var('py_version'), end='')")
PY_VERSION_NODOT=$($PYTHON -c "import sysconfig; print(sysconfig.get_config_var('py_version_nodot'), end='')")

PYTHON_TAG=cp$PY_VERSION_NODOT
if [[ $PY_PLATFORM == linux* ]]; then
    PLATFORM_TAG=many$(echo $PY_PLATFORM | sed 's/\-/_/')
    PLATFORM_TAG_MASK="$(echo $PLATFORM_TAG | sed 's/_/*_/')"
    if ! [ "$CI" == "true" ] && which podman >/dev/null; then
        export CIBW_CONTAINER_ENGINE=podman
    fi
else
    PLATFORM_TAG=$(echo $PY_PLATFORM | sed 's/\-/_/')
    PLATFORM_TAG_MASK="$(echo $PLATFORM_TAG | sed 's/_/*/')"
fi

# Usage
if ! [ -z "$1" ] && [ "$1" == "--help" ]; then
    echo "Usage:"
    echo "$0 [--all|TAG] [--archs=ARCHS]"
    echo "Where:"
    echo "  --all         Build all valid wheels for current OS."
    echo "  TAG           Force build the wheel for the given identifier."
    echo "                [default: $PYTHON_TAG-$PLATFORM_TAG]"
    echo "  --archs=ARCHS Comma-separated list of CPU architectures to build for."
    exit 1
fi

BUILD_TAG="--only"
ARCHS=""
while ! [ -z "$1" ]; do
    if [ "$1" == "--all" ]; then
        BUILD_TAG=""
    elif [[ $1 == --archs=* ]]; then
        ARCHS=$1
        if [ "$BUILD_TAG" == "--only" ]; then
            BUILD_TAG=""
        fi
    else
        BUILD_TAG="$1"
    fi
    shift
done

# Functions and commands
_verlte() {
    echo -e $(echo -e "$1\n$2" | sort -V | head -n1)
}

_vergte() {
    echo -e $(echo -e "$1\n$2" | sort -V -r | head -n1)
}

_bump_my_version () {
    local args=$*
    # Use python <= 3.12 (python 3.13t is not supported)
    local py_version=$(_verlte $PY_VERSION 3.12)
    echo $(uvx -p $py_version bump-my-version $args 2>/dev/null | tr -d '\r\n')
}

_cibuildwheel () {
    local args=$*
    # Use python >= 3.11
    local py_version=$(_vergte $PY_VERSION 3.11)
    # Do not export UV_* to avoid conflict with uv in cibuildwheel macOS/Windows
    unset UV_SYSTEM_PYTHON
    uvx -p $py_version cibuildwheel $args
}

echo "::group::Install dependencies and build tools"
UV_RESOLUTION=highest uv pip install -r requirements.txt
VERSION=$(_bump_my_version show current_version)
if [[ $VERSION == *-* ]]; then
    VERSION_OK=$($PYTHON -c "print(''.join('$VERSION'.replace('-','.').rsplit('.',1)), end='')")
else
    VERSION_OK=$VERSION
fi
echo "::endgroup::"

mkdir -p wheelhouse >/dev/null
if [[ $PY_PLATFORM == linux* ]]; then
    echo "::group::Build sdist"
    uv build --no-build-isolation --sdist -o wheelhouse
    echo "::endgroup::"
fi
echo "::group::Build wheel(s)"
if [ "$BUILD_TAG" == "--only" ]; then
    DIRTY=$(_bump_my_version show scm_info.dirty)
    FILEMASK="cx_Freeze-$VERSION_OK-$PYTHON_TAG-$PYTHON_TAG-$PLATFORM_TAG_MASK"
    FILEEXISTS=$(ls "wheelhouse/$FILEMASK.whl" 2>/dev/null || echo '')
    if [ "$DIRTY" != "False" ] || [ -z "$FILEEXISTS" ]; then
        if [[ $PY_PLATFORM == win* ]]; then
            uv build --no-build-isolation  --wheel -o wheelhouse
        else
            _cibuildwheel --only "$PYTHON_TAG-$PLATFORM_TAG"
        fi
    fi
elif ! [ -z "$BUILD_TAG" ]; then
    CIBW_BUILD="$BUILD_TAG" _cibuildwheel $ARCHS
else
    _cibuildwheel $ARCHS
fi
echo "::endgroup::"

if ! [ "$CI" == "true" ]; then
    echo "::group::Install cx_Freeze $VERSION_OK"
    UV_PYTHON=$UV_PYTHON UV_PRERELEASE=allow \
        uv pip install "cx_Freeze==$VERSION_OK" --no-index --no-deps -f wheelhouse --reinstall
    echo "::endgroup::"
fi
