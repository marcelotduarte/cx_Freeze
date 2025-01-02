#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage:"
    echo "$0 sample [--system|--venv] [--deps=x] [--debug] [--verbose]"
    echo "Where:"
    echo "  sample is the name in samples directory (e.g. cryptography)"
    echo "  --system is an option to use system python"
    echo "  --venv is an option to use python in a virtual environment"
    echo "  --deps=b,d,e,l,p,n - install package dependencies"
    echo "         b=basic - only dependencies to build cx_Freeze"
    echo "         d=dist - build a distributable cx_Freeze (cibuildwheel for now)"
    echo "         e=editable - build cx_Freeze in editable (develop) mode"
    echo "         l=latest - use the latest version of cx_Freeze in pypi or conda"
    echo "         p=packages - use the pre release version of cx_Freeze in packages site"
    echo "         n=no - disable installing package dependencies"
    echo "  --no-deps - same as --deps=n"
    echo "  --debug - enable debug variables"
    echo "  --debug-plugins - enable debug plugins (mostly for qt)"
    echo "  --verbose - enable verbose mode (for now to build cx_Freeze)"
    exit 1
fi

echo "::group::Prepare the environment"
# Presume unexpected error
TEST_SAMPLE=$1
TEST_VENV=""
TEST_DEPS=""
TEST_DEBUG=""
TEST_DEVELOP=""
TEST_VERBOSE=""
while ! [ -z "$2" ]; do
    if [ "$2" == "--system" ] || [ "$2" == "--venv" ]; then
        TEST_VENV="$2"
    elif [ "$2" == "--deps=b" ]; then
        TEST_DEPS="--basic-requirements"
    elif [ "$2" == "--deps=d" ]; then
        TEST_DEVELOP="--dist"
    elif [ "$2" == "--deps=e" ]; then
        TEST_DEVELOP="--editable"
    elif [ "$2" == "--deps=l" ]; then
        TEST_DEVELOP="--latest"
    elif [ "$2" == "--deps=p" ]; then
        TEST_DEPS=""
    elif [ "$2" == "--deps=n" ] || [ "$2" == "--no-deps" ]; then
        TEST_DEPS="no"
    elif [ "$2" == "--debug" ]; then
        TEST_DEBUG="$2"
        export QT_DEBUG=1
        export QT_WIN_DEBUG_CONSOLE=1
        export QT_LOGGING_RULES='qt.webengine*.debug=true'
    elif [ "$2" == "--debug-plugins" ]; then
        export QT_DEBUG_PLUGINS=1
    elif [ "$2" == "--verbose" ]; then
        TEST_VERBOSE="$2"
    else
        echo "WARNING: no such option: $2"
    fi
    shift
done
if [ -z "$TEST_VENV" ] && [ "$CONDA_DEFAULT_ENV" == "base" ]; then
    TEST_VENV="--venv"
fi
if [ -z "$CONDA_DEFAULT_ENV" ] &&
   [ -z "$GITHUB_WORKSPACE" ] &&
   [ -z "$MSYSTEM_PREFIX" ] &&
   [ -z "$VIRTUAL_ENV" ] &&
   [ -z "$TEST_VENV" ]
then
    echo "ERROR: Required the use of a virtual environment."
    echo "::endgroup::"
    exit 1
fi

# Get script directory (without using /usr/bin/realpath)
CI_DIR=$(cd `dirname "${BASH_SOURCE[0]}"` && pwd)
# This script is on ci subdirectory
TOP_DIR=$(cd "$CI_DIR/.." && pwd)
# Get build utilities
source "$CI_DIR/build-utils.sh"
# Verifiy if python is installed
PYTHON=$(get_python)
if [ -z $PYTHON ]; then
    echo $(get_python_error)
    exit 1
fi
if ! [ -z "$CONDA_PYTHON_EXE" ]; then
    BASE_PYTHON=$CONDA_PYTHON_EXE
else
    BASE_PYTHON=$PYTHON
fi
if [ "$TEST_VENV" == "--system" ]; then
    export UV_SYSTEM_PYTHON=1
else
    export UV_PYTHON=$($PYTHON -c "import sys; print(sys.executable, end='')")
fi
# Python information (platform and version)
PY_PLATFORM=$($PYTHON -c "import sysconfig; print(sysconfig.get_platform(), end='')")
PY_VERSION=$($PYTHON -c "import sysconfig; print(sysconfig.get_python_version(), end='')")
PY_VERSION_FULL=$($PYTHON -c "import sysconfig; print(sysconfig.get_config_var('py_version'), end='')")
PY_VERSION_NODOT=$($PYTHON -c "import sysconfig; print(sysconfig.get_config_var('py_version_nodot'), end='')")
echo "Environment:"
echo "    Platform $PY_PLATFORM"
echo "    Python version $PY_VERSION_FULL"
if ! [ -z "$CONDA_EXE" ]; then
    CONDA_VERSION=$($PYTHON -c "print('`$CONDA_EXE --version`'.split(' ')[1])")
    echo "    Conda version $CONDA_VERSION"
fi
echo "::endgroup::"

echo "::group::Check if $TEST_SAMPLE sample exists"
# Check if samples are in the current directory or in a cx_Freeze tree
if [ -d "$TEST_SAMPLE" ]; then
    TEST_DIR=$(cd "$TEST_SAMPLE" && pwd)
else
    TEST_DIR="${TOP_DIR}/samples/$TEST_SAMPLE"
fi
if ! [ -d "$TEST_DIR" ]; then
    echo "ERROR: Sample's directory NOT found"
    echo "::endgroup::"
    exit 1
fi
echo "INFO: The sample is available for test at $TEST_DIR"
pushd "$TEST_DIR" >/dev/null
if [ "$TEST_VENV" == "--venv" ]; then
    if [[ $PY_PLATFORM == mingw* ]]; then
        echo "WARNING: ignoring --venv in MSYS2 environment"
    elif ! [ -z "$CONDA_DEFAULT_ENV" ] && ! [ "$CONDA_DEFAULT_ENV" == "base" ]; then
        echo "WARNING: ignoring --venv, using CONDA $CONDA_DEFAULT_ENV environment"
    else
        [ -z "$HOME" ] && HOME=$PWD
        VENV_NAME="cxfreeze_${TEST_SAMPLE}_${PY_PLATFORM}_${PY_VERSION_NODOT}"
        if ! [ -z "$CONDA_EXE" ]; then
            if ! $($CONDA_EXE env list | grep -q $VENV_NAME); then
                echo "Create conda env $VENV_NAME"
                $CONDA_EXE create -c conda-forge -n $VENV_NAME python=$PY_VERSION -y
                # on create env install dependencies
                TEST_DEPS=""
            fi
            echo "Run: conda activate $VENV_NAME"
            if [ "$OSTYPE" == "msys" ]; then
                source $(dirname $BASE_PYTHON)/Scripts/activate $VENV_NAME
                PYTHON=$(cygpath -u "$CONDA_PREFIX/python.exe")
            else
                source $(dirname $BASE_PYTHON)/activate $VENV_NAME
                PYTHON="$CONDA_PREFIX/bin/python"
            fi
        else
            # use brew python in macOS
            #if ! [ -z "$GITHUB_WORKSPACE" ] && which brew; then
            #    PYTHON=$(brew --prefix)/opt/python@$PY_VERSION/libexec/bin/python
            #fi
            VENV_LOCAL="${HOME}/.local/venv/${VENV_NAME}"
            if ! [ -d $VENV_LOCAL ]; then
                echo "Create venv $VENV_LOCAL"
                if which uv &>/dev/null; then
                    uv venv $VENV_LOCAL
                else
                    $PYTHON -m venv $VENV_LOCAL
                fi
                # on create env install dependencies
                TEST_DEPS=""
            fi
            echo "Activate venv $VENV_LOCAL"
            if [[ $PY_PLATFORM == win* ]]; then
                PYTHON="${VENV_LOCAL}/Scripts/python.exe"
            else
                source "${VENV_LOCAL}/bin/activate"
                PYTHON=`which python`
            fi
            export UV_PYTHON=$($PYTHON -c "import sys; print(sys.executable, end='')")
        fi
        # update python platform and version based on active virtual env
        PY_PLATFORM=$($PYTHON -c "import sysconfig; print(sysconfig.get_platform(), end='')")
        PY_VERSION=$($PYTHON -c "import sysconfig; print(sysconfig.get_python_version(), end='')")
        PY_VERSION_NODOT=$($PYTHON -c "import sysconfig; print(sysconfig.get_config_var('py_version_nodot'), end='')")
    fi
fi
echo "::endgroup::"

echo "::group::Install platform specific utilities/packages"
# started before the build because qt, tk and wx depend on $DISPLAY
install_x11_tools $PY_PLATFORM
install_docker_or_podman $PY_PLATFORM
install_screen_capture $PY_PLATFORM
install_xvfb $PY_PLATFORM
start_xvfb $PY_PLATFORM
echo "::endgroup::"
if [ "$CI" == "true" ] && [[ $PY_PLATFORM == linux* ]]; then
    echo "::group::List platform specific utilities/packages"
    dpkg -l --no-pager
    echo "::endgroup::"
fi

echo "::group::Install dependencies for $TEST_SAMPLE sample"
if [ "$TEST_DEPS" != "no" ]; then
    export PIP_DISABLE_PIP_VERSION_CHECK=1
    set -x
    $PYTHON "$CI_DIR/build_test.py" \
        $TEST_SAMPLE $TEST_DEPS $TEST_DEVELOP $TEST_DEBUG $TEST_VERBOSE
    set +x
else
    echo "INFO: Skipping"
fi

CXFREEZE_VERSION=$(cx_freeze_version "$PYTHON")
echo "::endgroup::"
if [ -z "$CXFREEZE_VERSION" ]; then
    exit 1
fi

echo -n "::group::Show packages "
if ! [ -z "$CONDA_DEFAULT_ENV" ]; then
    echo "(conda list)"
    $CONDA_EXE run -n $CONDA_DEFAULT_ENV python -VV
    $CONDA_EXE list -n $CONDA_DEFAULT_ENV
elif [[ $PY_PLATFORM == mingw* ]]; then
    echo "(pacman -Q && pip list -v)"
    filter=$($PYTHON -c "print('$PY_PLATFORM'.replace('_', '-w64-', 1), end='')")
    pacman -Q | grep "${filter}-python"
    $PYTHON -m pip list -v
else
    echo "(pip list -v)"
    if which uv &>/dev/null; then
        uv pip list -v
    else
        $PYTHON -VV
        $PYTHON -m pip list -v
    fi
fi
echo "::endgroup::"

echo "::group::Freeze $TEST_SAMPLE sample (cx_Freeze $CXFREEZE_VERSION)"
# Set build_exe options
TEST_OPTIONS="--silent"
if [ "$TEST_SAMPLE" != "tkinter" ] && [ ! -z "${TEST_SAMPLE##*_tk}" ]; then
    TEST_OPTIONS="$TEST_OPTIONS --excludes=tkinter"
fi
if [[ $PY_PLATFORM == win* ]]; then
    TEST_OPTIONS="$TEST_OPTIONS --include-msvcr"
fi
# Validate bdist actions
if [[ $PY_PLATFORM == linux* ]]; then
    if [ "$TEST_BDIST" != "bdist_appimage" ] && [ "$TEST_BDIST" != "bdist_rpm" ]; then
        TEST_BDIST=
    fi
elif [[ $PY_PLATFORM == macos* ]]; then
    if [ "$TEST_BDIST" != "bdist_mac" ] && [ "$TEST_BDIST" != "bdist_dmg" ]; then
        TEST_BDIST=
    fi
elif [[ $PY_PLATFORM == win* ]] || [[ $PY_PLATFORM == mingw* ]]; then
    if [ "$TEST_BDIST" != "bdist_msi" ]; then
        TEST_BDIST=
    fi
else
    TEST_BDIST=
fi
# Freeze
if [ -f setup.py ]; then
    CXFREEZE_CMD="$PYTHON setup.py $TEST_VERBOSE"
else
    PY_SCRIPT=$($PYTHON -c "import sysconfig; print(sysconfig.get_path('scripts'), end='')")
    CXFREEZE_CMD="$PY_SCRIPT/cxfreeze"
fi
echo "$CXFREEZE_CMD build_exe $TEST_OPTIONS $TEST_BDIST"
$CXFREEZE_CMD build_exe $TEST_OPTIONS $TEST_BDIST
TEST_EXITCODE=$?
popd >/dev/null
echo "::endgroup::"
if ! [ "$TEST_EXITCODE" == "0" ]; then
    exit $TEST_EXITCODE
fi

echo "::group::Prepare to run the $TEST_SAMPLE sample"
BUILD_DIR="${TEST_DIR}/build/exe.${PY_PLATFORM}-${PY_VERSION}"
BUILD_DIRS=("$BUILD_DIR" "--" "--")
if [ "$TEST_BDIST" == "bdist_mac" ] || [ "$TEST_BDIST" == "bdist_dmg" ]; then
    # add the app name if run on bdist_mac
    names=(${TEST_DIR}/build/*.app)
    BUILD_DIRS=("$BUILD_DIR" "${names[0]}/Contents/MacOS" "${names[0]}")
fi
for i in 0 1 2; do
    BUILD_DIR=${BUILD_DIRS[$i]}
    if ! [ -d "$BUILD_DIR" ]; then
        break
    fi
    pushd "$BUILD_DIR" >/dev/null
    TEST_EXITCODE_FAIL=0
    count=0
    # use the original PYTHON, not the virtual environment PYTHON
    echo BASE_PYTHON=$BASE_PYTHON
    $BASE_PYTHON "$CI_DIR/build_run.py" $TEST_SAMPLE --directory="$BUILD_DIR" |\
    while IFS= read -r TEST_RUN; do
        TEST_RUN_ARGV=(${TEST_RUN})

        if [ "${TEST_RUN_ARGV[0]}" == "status" ]; then
            TEST_EXITCODE_FAIL=${TEST_RUN_ARGV[1]}
            break
        fi

        TEST_PID=${TEST_RUN_ARGV[0]}
        TEST_EXITCODE=${TEST_RUN_ARGV[1]}
        TEST_LOG=${TEST_RUN_ARGV[2]}.log
        TEST_ERR=${TEST_RUN_ARGV[2]}.err
        TEST_APPTYPE=${TEST_RUN_ARGV[3]}
        TEST_NAME="${TEST_RUN_ARGV[4]}"
        if [[ $TEST_NAME == b64:* ]]; then
            TEST_B64=$(echo "${TEST_NAME:4}")
            TEST_NAME=$($PYTHON -c "from base64 import b64decode; print(b64decode('$TEST_B64').decode(), end='')")
        fi

        echo "::endgroup::"
        if ! [ -z "$TEST_LOG" ] && [ -f "$TEST_LOG" ]; then
            if [[ $PY_PLATFORM == mingw* ]] && [ "$CI" == "true" ]; then
                (mintty --title "$TEST_NAME" --hold always --exec cat "$TEST_LOG")&
            else
                echo -n "::group::"
                cat "$TEST_LOG"
                echo "::endgroup::"
            fi
        fi
        if ! [ -z "$TEST_ERR" ] && [ -f "$TEST_ERR" ]; then
            echo "::group::Print $TEST_ERR"
            cat "$TEST_ERR"
            echo "::endgroup::"
        fi
        if [[ $PY_PLATFORM == linux* ]] && [ "$TEST_APPTYPE" == "cui" ]; then
            echo "::group::Run '$TEST_NAME' sample in docker"
            echo `printf '=%.0s' {1..40}`
            TEST_DOCKER=/frozen/$(basename $TEST_NAME)
            DOCKER_APP=`which podman`
            if [ -z "$DOCKER_APP" ]; then
                DOCKER_APP=`which docker`
            fi
            if ! [ -z "$DOCKER_APP" ]; then
                $DOCKER_APP run --rm -t \
                    -v `pwd`:/frozen ubuntu:20.04 $TEST_DOCKER
            else
                echo "INFO: Neither podman nor docker installed."
            fi
            echo `printf '=%.0s' {1..40}`
            echo "::endgroup::"
        fi
        echo "::group::Prepare to run the next $TEST_SAMPLE sample"
        count=$(( $count + 1 ))
    done
    popd >/dev/null
done
kill_xvfb $PY_PLATFORM
echo "status=$TEST_EXITCODE_FAIL"
echo "::endgroup::"
exit $TEST_EXITCODE_FAIL
