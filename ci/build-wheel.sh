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
    PLATFORM_TAG_MASK=$(echo $PLATFORM_TAG | sed 's/_/*_/')
    if ! [ "$CI" == "true" ] && which podman >/dev/null; then
        export CIBW_CONTAINER_ENGINE=podman
    fi
else
    PLATFORM_TAG=$(echo $PY_PLATFORM | sed 's/\-/_/')
    PLATFORM_TAG_MASK=$(echo $PLATFORM_TAG | sed 's/_/*/')
fi

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
        BUILD_TAG=$1
    fi
    shift
done

echo "::group::Install dependencies and build tools"
# Do not export UV_PYTHON to avoid conflict with uv in cibuildwheel macOS
UV_RESOLUTION=highest \
    uv pip install -r requirements.txt -r requirements-dev.txt
VERSION=$(bump-my-version show current_version 2>/dev/null | tr -d '\r\n')
echo "::endgroup::"

mkdir -p wheelhouse >/dev/null
if [[ $PY_PLATFORM == linux* ]]; then
    echo "::group::Build sdist"
    uv build --no-build-isolation --sdist -o wheelhouse
    echo "::endgroup::"
fi
echo "::group::Build wheel(s)"
# Do not export UV_* to avoid conflict with uv in cibuildwheel macOS/Windows
unset UV_PYTHON
unset UV_SYSTEM_PYTHON
if [ "$BUILD_TAG" == "--only" ]; then
    VERSION_BASE=$($PYTHON -c "print('$VERSION'.rsplit('-',1)[0], end='')")
    DIRTY=$(bump-my-version show scm_info.dirty 2>/dev/null | tr -d '\r\n')
    FILEMASK=cx_Freeze-$VERSION_BASE*-$PYTHON_TAG-$PYTHON_TAG-$PLATFORM_TAG_MASK
    FILEEXISTS=$(ls wheelhouse/$FILEMASK.whl 2>/dev/null || echo '')
    if [ "$DIRTY" == "True" ] || [ -z "$FILEEXISTS" ]; then
        if [[ $PY_PLATFORM == win* ]]; then
            uv build --no-build-isolation  --wheel -o wheelhouse
        else
            cibuildwheel --only $PYTHON_TAG-$PLATFORM_TAG --prerelease-pythons
        fi
    fi
elif ! [ -z "$BUILD_TAG" ]; then
    CIBW_BUILD="$BUILD_TAG" cibuildwheel $ARCHS
else
    cibuildwheel $ARCHS
fi
echo "::endgroup::"

if ! [ "$CI" == "true" ]; then
    VERSION_OK=$($PYTHON -c "print(''.join('$VERSION'.replace('-','.').rsplit('.',1)), end='')")
    echo "::group::Install cx_Freeze $VERSION_OK"
    UV_PYTHON=$UV_PYTHON UV_PRERELEASE=allow \
        uv pip install "cx_Freeze==$VERSION_OK" --no-index --no-deps -f wheelhouse --reinstall
    echo "::endgroup::"
fi
