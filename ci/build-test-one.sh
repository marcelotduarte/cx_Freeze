#!/bin/bash

if [ -z "$CONDA_DEFAULT_ENV" ] &&
   [ -z "$GITHUB_WORKSPACE" ] &&
   [ -z "$VIRTUAL_ENV" ] && [ -z "$2" ]
then
    echo "Required: use of a virtual environment."
    exit 1
fi

if [ -z "$1" ] ; then
    echo "Usage: $0 sample [--pipenv | --venv] [--no-deps]"
    echo "Where:"
    echo "  sample is the name in samples directory (e.g. cryptography)"
    echo "  --pipenv is an option to enable pipenv usage"
    echo "  --venv is an option to enable python venv module usage"
    echo "  --no-deps - disable installing package dependencies"
    echo "  --debug - enable debug variables"
    exit 1
fi

# Verifiy if python is installed
if ! [ -z `which python` ] ; then
    PYTHON=`which python`
elif ! [ -z `which python3` ] ; then
    PYTHON=python3
else
    echo "ERROR: python not found"
    exit 1
fi
BASE_PYTHON=$PYTHON

echo "::group::Prepare the environment"
# Presume unexpected error
TEST_SAMPLE=$1
MANAGER=""
INSTALL_DEPS=yes
TEST_DEBUG=""
while ! [ -z "$2" ] ; do
    if [ "$2" == "--pipenv" ] || [ "$2" == "--venv" ] ; then
        MANAGER="$2"
    elif [ "$2" == "--no-deps" ] ; then
        INSTALL_DEPS=no
    elif [ "$2" == "--debug" ] ; then
        TEST_DEBUG="$2"
        export QT_DEBUG=1
        export QT_DEBUG_PLUGINS=1
    else
        echo "WARNING: no such option: $2"
    fi
    shift
done
# Get script directory (without using /usr/bin/realpath)
CI_DIR=$(cd `dirname "${BASH_SOURCE[0]}"` && pwd)
# This script is on ci subdirectory
TOP_DIR=$(cd "$CI_DIR/.." && pwd)
# Get build utilities
source $CI_DIR/build-utils.sh
# python information (platform and version)
PY_PLATFORM=$($PYTHON -c "import sysconfig; print(sysconfig.get_platform())")
PY_VERSION=$($PYTHON -c "import sysconfig; print(sysconfig.get_python_version())")
# Validate bdist_mac action
if ! [[ $PY_PLATFORM == macos* ]] || [ -z "$TEST_BDIST_MAC" ] ; then
    TEST_BDIST_MAC=0
fi
echo "Environment:"
echo "    Platform $PY_PLATFORM"
echo "    Python version $PY_VERSION"
if ! [ -z "$CONDA_EXE" ] ; then
    echo "    $($CONDA_EXE --version)"
fi
echo "::endgroup::"

echo "::group::Check if $TEST_SAMPLE sample exists"
# Check if the samples is in current directory or in a cx_Freeze tree
if [ -d "$TEST_SAMPLE" ] ; then
    TEST_DIR=$(cd "$TEST_SAMPLE" && pwd)
else
    TEST_DIR="${TOP_DIR}/samples/$TEST_SAMPLE"
fi
if ! [ -d "$TEST_DIR" ] ; then
    echo "ERROR: Sample's directory NOT found"
    echo "::endgroup::"
    exit 1
fi
echo "INFO: The sample is available for test at $TEST_DIR"
pushd "$TEST_DIR" >/dev/null
if [ "$MANAGER" == "--pipenv" ] ; then
    [ -z `which pipenv` ] && $PYTHON -m pip install --upgrade pipenv
    if [ -z `which pipenv` ] ; then
        echo "ERROR: pipenv NOT available"
        echo "::endgroup::"
        exit 1
    fi
    PIPENV="$PYTHON -m pipenv"
    export PIPENV_NO_INHERIT=1
    if [ -z `$PIPENV --venv` ] ; then
        rm Pipfile 2>/dev/null || true
        rm Pipfile.lock 2>/dev/null || true
        if [ "$OSTYPE" == "msys" ] ; then
            $PIPENV --python $(cygpath -w `which python`)
        else
            $PIPENV --python $(which $PYTHON) --no-site-packages
        fi
    fi
    PYTHON="$PIPENV run python"
elif [ "$MANAGER" == "--venv" ] ; then
    VENV_NAME=cx_Freeze_${TEST_SAMPLE}_py${PY_VERSION}_${PY_PLATFORM}
    [ -z "$HOME" ] && HOME=$PWD
    VENV_LOCAL=${HOME}/.local/venv/$VENV_NAME
    $PYTHON -m venv $VENV_LOCAL
    if [[ $PY_PLATFORM == win* ]] ; then
        PYTHON=$VENV_LOCAL/Scripts/python.exe
    else
        source $VENV_LOCAL/bin/activate
        PYTHON=python
    fi
fi
echo "::endgroup::"

echo "::group::Install platform specific utilities/packages"
# started before the build because tk (and qt) depend on $DISPLAY
install_xvfb $PY_PLATFORM
start_xvfb $PY_PLATFORM
install_screen_capture $PY_PLATFORM
install_x11_tools $PY_PLATFORM
install_docker_or_podman $PY_PLATFORM
echo "::endgroup::"

echo "::group::Install dependencies for $TEST_SAMPLE sample"
if [ "$INSTALL_DEPS" == "yes" ] ; then
    export PIP_DISABLE_PIP_VERSION_CHECK=1
    $PYTHON "${CI_DIR}/build_test.py" $TEST_SAMPLE --all-requirements
    if ! [ -z "$CONDA_PREFIX" ] && [ -z $(cx_freeze_version "$PYTHON") ] ; then
        # somentimes in conda, occurs error 247 if occurs downgrade of python
        $PYTHON "${CI_DIR}/build_test.py" $TEST_SAMPLE --all-requirements
    fi
else
    echo "INFO: Skipping"
fi

CXFREEZE_VERSION=$(cx_freeze_version "$PYTHON")
echo "::endgroup::"
if [ -z "$CXFREEZE_VERSION" ] ; then
    exit 1
fi

echo -n "::group::Show packages "
if [ "$MANAGER" == "--pipenv" ] ; then
    echo "(pipenv graph)"
    $PYTHON -VV
    $PIPENV --venv
    echo `printf '=%.0s' {1..40}`
    $PIPENV graph
elif ! [ -z "$CONDA_DEFAULT_ENV" ] ; then
    echo "(conda list)"
    $CONDA_EXE run -n $CONDA_DEFAULT_ENV python -VV
    $CONDA_EXE list -n $CONDA_DEFAULT_ENV
elif [[ $PY_PLATFORM == mingw* ]] ; then
    echo "(pacman -Q && pip list -v)"
    filter=$($PYTHON -c "print('$PY_PLATFORM'.replace('_', '-w64-', 1))")
    pacman -Q | grep "${filter}-python"
    $PYTHON -m pip list -v
else
    echo "(pip list -v)"
    $PYTHON -VV
    $PYTHON -m pip list -v
fi
echo "::endgroup::"

echo "::group::Freeze $TEST_SAMPLE sample (cx_Freeze $CXFREEZE_VERSION)"
TEST_OPTIONS="--silent"
if [ "$TEST_SAMPLE" != "tkinter" ] && [ ! -z "${TEST_SAMPLE##*_tk}" ] ; then
    TEST_OPTIONS="$TEST_OPTIONS --excludes=tkinter"
fi
if [[ $PY_PLATFORM == win* ]] ; then
    TEST_OPTIONS="$TEST_OPTIONS --include-msvcr=true"
fi
if [ "$TEST_BDIST_MAC" != "0" ]; then
    $PYTHON setup.py build_exe $TEST_OPTIONS bdist_mac
else
    $PYTHON setup.py build_exe $TEST_OPTIONS
fi
TEST_EXITCODE=$?
popd >/dev/null
echo "::endgroup::"
if ! [ "$TEST_EXITCODE" == "0" ] ; then
    exit $TEST_EXITCODE
fi

echo "::group::Prepare to run the $TEST_SAMPLE sample"
BUILD_DIR="${TEST_DIR}/build/exe.${PY_PLATFORM}-${PY_VERSION}"
pushd "${BUILD_DIR}" >/dev/null
TEST_EXITCODE_FAIL=0
count=0
# use the original PYTHON, not the virtual environment PYTHON
echo PYTHON=$BASE_PYTHON
$BASE_PYTHON "${CI_DIR}/build_run.py" $TEST_SAMPLE | while IFS= read -r TEST_RUN; do
    #echo TEST_RUN=$TEST_RUN
    TEST_RUN_ARGV=(${TEST_RUN})

    if [ "${TEST_RUN_ARGV[0]}" == "status" ] ; then
        TEST_EXITCODE_FAIL=${TEST_RUN_ARGV[1]}
        break
    fi

    TEST_PID=${TEST_RUN_ARGV[0]}
    TEST_EXITCODE=${TEST_RUN_ARGV[1]}
    TEST_LOG=${TEST_RUN_ARGV[2]}.log
    TEST_ERR=${TEST_RUN_ARGV[2]}.err
    TEST_APPTYPE=${TEST_RUN_ARGV[3]}
    TEST_NAME=${TEST_RUN_ARGV[4]}
    if [[ $TEST_NAME == b64:* ]] ; then
        TEST_NAME=$($PYTHON -c "from base64 import b64decode; print(b64decode('${TEST_NAME:4}').decode())")
    fi

    # check the app type and remove that info from the app name
    # get the full name for some cases
    if [ "$TEST_BDIST_MAC" != "0" ] ; then
        # adjust the app name if run on bdist_mac
        names=(../*.app)
        TEST_DIR_BDIST=$(cd "${names[0]}/Contents/MacOS" && pwd)
        TEST_NAME_FULL="$TEST_DIR_BDIST/$TEST_NAME"
        # fix argv
        TEST_NAME_ARGV=(${TEST_NAME_FULL})
    fi

    echo "::endgroup::"
    if ! [ -z "$TEST_LOG" ] && [ -f "$TEST_LOG" ] ; then
        if [[ $PY_PLATFORM == mingw* ]] && [ "$CI" == "true" ] ; then
            (mintty --title "$TEST_NAME" --hold always --exec cat "$TEST_LOG")&
        else
            echo -n "::group::"
            cat "$TEST_LOG"
            echo "::endgroup::"
        fi
    fi
    if ! [ -z "$TEST_ERR" ] && [ -f "$TEST_ERR" ] ; then
        echo "::group::Print $TEST_ERR"
        cat "$TEST_ERR"
        echo "::endgroup::"
    fi
    if [[ $PY_PLATFORM == linux* ]] && [ "$TEST_APPTYPE" == "cui" ] ; then
        if ! [ "$MANAGER" == "--pipenv" ] ; then
            echo "::group::Run '$TEST_NAME' sample in docker"
            echo `printf '=%.0s' {1..40}`
            TEST_DOCKER=/frozen/$TEST_NAME
            docker run --rm -t -v `pwd`:/frozen ubuntu:18.04 $TEST_DOCKER
            echo `printf '=%.0s' {1..40}`
            echo "::endgroup::"
        fi
    fi
    echo "::group::Prepare to run the next $TEST_SAMPLE sample"
    count=$(( $count + 1 ))
done
popd >/dev/null
kill_xvfb $PY_PLATFORM
echo "status=$TEST_EXITCODE_FAIL"
echo "::endgroup::"
exit $TEST_EXITCODE_FAIL
