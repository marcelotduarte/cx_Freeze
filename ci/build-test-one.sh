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
TEST_DEBUG=
TEST_VERBOSE=
while [ -n "$2" ]; do
    if [ "$2" == "--system" ] || [ "$2" == "--venv" ]; then
        TEST_VENV="$2"
    elif [ "$2" == "--deps=b" ]; then
        TEST_DEPS="--basic-requirements"
    elif [ "$2" == "--deps=d" ]; then
        TEST_DEPS="--dist"
    elif [ "$2" == "--deps=e" ]; then
        TEST_DEPS="--editable"
    elif [ "$2" == "--deps=l" ]; then
        TEST_DEPS="--latest"
    elif [ "$2" == "--deps=p" ]; then
        TEST_DEPS="--packages"
    elif [ "$2" == "--deps=n" ] || [ "$2" == "--no-deps" ]; then
        TEST_DEPS="no"
    elif [ "$2" == "--debug" ]; then
        TEST_DEBUG=$2
        export QT_DEBUG=1
        export QT_WIN_DEBUG_CONSOLE=1
        export QT_LOGGING_RULES='qt.webengine*.debug=true'
    elif [ "$2" == "--debug-plugins" ]; then
        export QT_DEBUG_PLUGINS=1
    elif [ "$2" == "--verbose" ]; then
        TEST_VERBOSE=$2
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
_CI_DIR=$(dirname "${BASH_SOURCE[0]}")
CI_DIR=$(cd "$_CI_DIR" && pwd)
# This script is on ci subdirectory
TOP_DIR=$(cd "$CI_DIR/.." && pwd)
# Get build utilities
# shellcheck source=/dev/null
source "$CI_DIR/build-utils.sh"
# Verify if python is installed
PYTHON=$(get_python)
if [ -z "$PYTHON" ]; then
    get_python_error
    exit 1
fi
if [ -n "$CONDA_PYTHON_EXE" ]; then
    BASE_PYTHON=$CONDA_PYTHON_EXE
else
    BASE_PYTHON=$PYTHON
fi
# Python information (platform and version)
PY_PLATFORM=$($PYTHON -c "import sysconfig; print(sysconfig.get_platform(), end='')")
PY_VERSION=$($PYTHON -c "import sysconfig; print(sysconfig.get_python_version(), end='')")
PY_VERSION_FULL=$($PYTHON -c "import sysconfig; print(sysconfig.get_config_var('py_version'), end='')")
PY_VERSION_NODOT=$($PYTHON -c "import sysconfig; print(sysconfig.get_config_var('py_version_nodot'), end='')")
PY_ABI_THREAD=$($PYTHON -c "import sysconfig; print(sysconfig.get_config_var('abi_thread') or '', end='')")
IS_CONDA=$([ -n "$CONDA_EXE" ] && echo true)
IS_LINUX=$([[ $PY_PLATFORM == linux* ]] && echo true)
IS_MACOS=$([[ $PY_PLATFORM == macos* ]] && echo true)
#IS_MINGW=$([[ $PY_PLATFORM == cygwin* ]] || [[ $PY_PLATFORM == mingw* ]] && echo true)
IS_MINGW=$([[ $PY_PLATFORM == mingw* ]] && echo true)
IS_WINDOWS=$([[ $PY_PLATFORM == win* ]] && echo true)
#IS_WINE=$([ "$OSTYPE" == "linux-gnu" ] && [ "$IS_WINDOWS" == "true" ] && echo true)
echo "Environment:"
echo "    Platform $PY_PLATFORM"
echo "    Python version $PY_VERSION$PY_ABI_THREAD ($PY_VERSION_FULL)"
if [ "$IS_CONDA" == "true" ]; then
    CONDA_VERSION=$($PYTHON -c "print('$($CONDA_EXE --version)'.split(' ')[1])")
    echo "    Conda version $CONDA_VERSION"
fi
echo "::endgroup::"

echo "::group::Check if $TEST_SAMPLE sample exists"
# Check if samples are in the current directory or in a cx_Freeze tree
if [ -d "$TEST_SAMPLE" ]; then
    TEST_DIR=$(cd "$TEST_SAMPLE" && pwd)
else
    TEST_DIR="$TOP_DIR/samples/$TEST_SAMPLE"
fi
if ! [ -d "$TEST_DIR" ]; then
    echo "ERROR: Sample's directory NOT found"
    echo "::endgroup::"
    exit 1
fi
echo "INFO: The sample is available for test at $TEST_DIR"
pushd "$TEST_DIR" >/dev/null || exit 1
if [ "$TEST_VENV" == "--venv" ]; then
    if [ "$IS_MINGW" == "true" ]; then
        echo "WARNING: ignoring --venv in MSYS2 environment"
    elif [ "$IS_CONDA" == "true" ] && ! [ "$CONDA_DEFAULT_ENV" == "base" ]; then
        echo "WARNING: ignoring --venv, using CONDA $CONDA_DEFAULT_ENV environment"
    else
        [ -z "$HOME" ] && HOME=$PWD
        VENV_NAME="cxfreeze_${TEST_SAMPLE}_${PY_PLATFORM}_$PY_VERSION_NODOT$PY_ABI_THREAD"
        if [ "$IS_CONDA" == "true" ]; then
            if ! ($CONDA_EXE env list | grep -q "$VENV_NAME"); then
                echo "Create conda env $VENV_NAME"
                $CONDA_EXE create -c conda-forge -n "$VENV_NAME" \
                    python="$PY_VERSION$PY_ABI_THREAD" -y
                # on create env install dependencies
                if [ "$TEST_DEPS" == "no" ]; then
                    TEST_DEPS="--dist"
                fi
            fi
            echo "Run: conda activate $VENV_NAME"
            if [ "$OSTYPE" == "cygwin" ] || [ "$OSTYPE" == "msys" ]; then
                # shellcheck source=/dev/null
                source "$(dirname "$BASE_PYTHON")/Scripts/activate" "$VENV_NAME"
                PYTHON=$(cygpath -u "$CONDA_PREFIX/python.exe")
            else
                # shellcheck source=/dev/null
                source "$(dirname "$BASE_PYTHON")/activate" "$VENV_NAME"
                PYTHON="$CONDA_PREFIX/bin/python"
            fi
        else
            # use brew python in macOS
            #if ! [ -z "$GITHUB_WORKSPACE" ] && which brew; then
            #    PYTHON=$(brew --prefix)/opt/python@$PY_VERSION/libexec/bin/python
            #fi
            VENV_LOCAL="${HOME}/.local/venv/${VENV_NAME}"
            if ! [ -d "$VENV_LOCAL" ]; then
                echo "Create venv $VENV_LOCAL"
                if which uv &>/dev/null; then
                    uv venv -p "$PY_VERSION$PY_ABI_THREAD" "$VENV_LOCAL"
                else
                    $PYTHON -m venv "$VENV_LOCAL"
                fi
                # on create env install dependencies
                if [ "$TEST_DEPS" == "no" ]; then
                    TEST_DEPS="--dist"
                fi
            fi
            echo "Activate venv $VENV_LOCAL"
            if [ "$IS_WINDOWS" == "true" ]; then
                PYTHON="$VENV_LOCAL/Scripts/python.exe"
            else
                # shellcheck source=/dev/null
                source "$VENV_LOCAL/bin/activate"
                PYTHON=$(which python)
            fi
        fi
        # update python platform and version based on active virtual env
        PY_PLATFORM=$($PYTHON -c "import sysconfig; print(sysconfig.get_platform(), end='')")
        PY_VERSION=$($PYTHON -c "import sysconfig; print(sysconfig.get_python_version(), end='')")
        PY_VERSION_NODOT=$($PYTHON -c "import sysconfig; print(sysconfig.get_config_var('py_version_nodot'), end='')")
    fi
fi
if [ "$TEST_VENV" == "--system" ]; then
    export UV_SYSTEM_PYTHON=1
else
    UV_PYTHON=$($PYTHON -c "import sys; print(sys.executable, end='')")
    export UV_PYTHON
fi

echo "::endgroup::"

echo "::group::Install platform specific utilities/packages"
# started before the build because qt, tk and wx depend on $DISPLAY
install_x11_tools "$PY_PLATFORM"
install_docker_or_podman "$PY_PLATFORM"
install_screen_capture "$PY_PLATFORM"
install_xvfb "$PY_PLATFORM"
start_xvfb "$PY_PLATFORM"
echo "::endgroup::"

if [ "$CI" == "true" ] && [ "$IS_LINUX" == "true" ]; then
    echo "::group::List platform specific utilities/packages"
    dpkg -l --no-pager
    echo "::endgroup::"
fi

echo "::group::Install cx_Freeze and dependencies"
export PIP_DISABLE_PIP_VERSION_CHECK=1
if [ "$TEST_DEPS" != "no" ]; then
    # uninstall cx_Freeze
    if [ "$IS_CONDA" == "true" ]; then
        $CONDA_EXE remove -y --force-remove cx_freeze &>/dev/null || true
    elif [ "$IS_MINGW" == "true" ]; then
        pacman --noconfirm -R "$MINGW_PACKAGE_PREFIX-python-cx-freeze" &>/dev/null || true
    fi
    if which uv &>/dev/null; then
        uv pip uninstall cx_Freeze &>/dev/null || true
    else
        pip uninstall -y cx_Freeze &>/dev/null || true
    fi
    # install basic requirements
    if [ "$IS_CONDA" == "true" ] || [ "$IS_MINGW" == "true" ]; then
        # shellcheck disable=2086
        $PYTHON "$CI_DIR/build_test.py" \
            "$TEST_SAMPLE" --basic-requirements $TEST_DEBUG $TEST_VERBOSE
    fi
fi
pushd "$TOP_DIR" >/dev/null || exit 1
if [ "$TEST_DEPS" == "--dist" ]; then
    if [ "$IS_CONDA" == "true" ]; then
        pip install . --no-deps --no-cache-dir -vvv
    else
        "$CI_DIR/build-wheel.sh" --install
    fi
elif [ "$TEST_DEPS" == "--editable" ]; then
    if [ "$IS_CONDA" == "true" ] || \
       [ "$IS_MINGW" == "true" ] || \
       ! which uv &>/dev/null; then
        pip install -e. --no-build-isolation --no-deps
    else
        uv pip install --upgrade -r pyproject.toml
        uv pip install -e. --no-build-isolation --no-deps --reinstall
    fi
elif [ "$TEST_DEPS" == "--latest" ]; then
    if [ "$IS_CONDA" == "true" ]; then
        $CONDA_EXE install -y conda-forge::cx_freeze
    elif [ "$IS_MINGW" == "true" ]; then
        pacman -S --needed --noconfirm "$MINGW_PACKAGE_PREFIX-python-cx-freeze"
    elif which uv &>/dev/null; then
        uv pip install --upgrade cx_Freeze --reinstall
    else
        pip install --upgrade cx_Freeze
    fi
elif [ "$TEST_DEPS" == "--packages" ]; then
    PACKAGES_INDEX_URL="https://marcelotduarte.github.io/packages"
    if [ "$IS_CONDA" == "true" ]; then
        $CONDA_EXE install -y -c $PACKAGES_INDEX_URL/conda cx_freeze
    elif [ "$IS_MINGW" == "true" ]; then
        pacman -U --noconfirm "$MINGW_PACKAGE_PREFIX-python-cx-freeze"
    elif which uv &>/dev/null; then
        uv pip install --upgrade -r pyproject.toml
        uv pip install cx_Freeze --extra-index-url=$PACKAGES_INDEX_URL/ \
            --no-deps --prerelease=allow --reinstall
    else
        pip install cx_Freeze --index-url=$PACKAGES_INDEX_URL/ \
            --pre --force-reinstall
    fi
fi
popd >/dev/null || true
echo "::endgroup::"
echo "::group::Install dependencies for $TEST_SAMPLE sample"
if [ "$TEST_DEPS" != "no" ]; then
    # shellcheck disable=2086
    $PYTHON "$CI_DIR/build_test.py" "$TEST_SAMPLE" $TEST_DEBUG $TEST_VERBOSE
else
    echo "INFO: Skipping"
fi

CXFREEZE_VERSION=$(cx_freeze_version "$PYTHON")
if [ -z "$CXFREEZE_VERSION" ]; then
    echo "ERROR: cx_Freeze not found!"
    echo "::endgroup::"
    exit 1
fi
echo "::endgroup::"

echo -n "::group::Show packages "
if [ "$IS_CONDA" == "true" ]; then
    echo "(conda list)"
    $CONDA_EXE run -n "$CONDA_DEFAULT_ENV" python -VV
    $CONDA_EXE list -n "$CONDA_DEFAULT_ENV"
elif [ "$IS_MINGW" == "true" ]; then
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
if [ "$TEST_SAMPLE" != "tkinter" ] && [ -n "${TEST_SAMPLE##*_tk}" ]; then
    TEST_OPTIONS="$TEST_OPTIONS --excludes=tkinter"
fi
if [ "$IS_WINDOWS" == "true" ]; then
    TEST_OPTIONS="$TEST_OPTIONS --include-msvcr"
fi
# Validate bdist actions
if [ "$IS_LINUX" == "true" ]; then
    if [ "$TEST_BDIST" != "bdist_appimage" ] && [ "$TEST_BDIST" != "bdist_rpm" ]; then
        TEST_BDIST=
    fi
    if [ "$TEST_BDIST" == "bdist_appimage" ]; then
        TEST_OPTIONS="$TEST_OPTIONS --no-compress"
    fi
elif [ "$IS_MACOS" == "true" ]; then
    if [ "$TEST_BDIST" != "bdist_mac" ] && [ "$TEST_BDIST" != "bdist_dmg" ]; then
        TEST_BDIST=
    fi
elif [ "$IS_WINDOWS" == "true" ] || [ "$IS_MINGW" == "true" ]; then
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
# shellcheck disable=2086
$CXFREEZE_CMD build_exe $TEST_OPTIONS $TEST_BDIST
TEST_EXITCODE=$?
popd >/dev/null || true
echo "::endgroup::"
if ! [ "$TEST_EXITCODE" == "0" ]; then
    exit $TEST_EXITCODE
fi

echo "::group::Prepare to run the $TEST_SAMPLE sample"
BUILD_DIR="$TEST_DIR/build/exe.$PY_PLATFORM-$PY_VERSION$PY_ABI_THREAD"
BUILD_DIRS=("$BUILD_DIR" "--" "--")
if [ "$TEST_BDIST" == "bdist_mac" ] || [ "$TEST_BDIST" == "bdist_dmg" ]; then
    # add the app name if run on bdist_mac
    names=("$TEST_DIR/build/*.app")
    BUILD_DIRS=("$BUILD_DIR" "${names[0]}/Contents/MacOS" "${names[0]}")
fi
for i in 0 1 2; do
    BUILD_DIR=${BUILD_DIRS[$i]}
    if ! [ -d "$BUILD_DIR" ]; then
        break
    fi
    pushd "$BUILD_DIR" >/dev/null || exit 1
    TEST_EXITCODE_FAIL=0
    count=0
    # use the original PYTHON, not the virtual environment PYTHON
    echo "BASE_PYTHON=$BASE_PYTHON"
    while read -r -a TEST_RUN_ARGV; do
        if [ "${TEST_RUN_ARGV[0]}" == "status" ]; then
            TEST_EXITCODE_FAIL=${TEST_RUN_ARGV[1]}
            break
        fi

        # shellcheck disable=2034
        TEST_PID=${TEST_RUN_ARGV[0]}
        TEST_EXITCODE=${TEST_RUN_ARGV[1]}
        TEST_LOG=${TEST_RUN_ARGV[2]}.log
        TEST_ERR=${TEST_RUN_ARGV[2]}.err
        TEST_APPTYPE=${TEST_RUN_ARGV[3]}
        TEST_NAME="${TEST_RUN_ARGV[4]}"
        if [[ $TEST_NAME == b64:* ]]; then
            TEST_B64="${TEST_NAME:4}"
            TEST_NAME=$($PYTHON -c "from base64 import b64decode; print(b64decode('$TEST_B64').decode(), end='')")
        fi

        echo "::endgroup::"
        if [ -n "$TEST_LOG" ] && [ -f "$TEST_LOG" ]; then
            if [ "$IS_MINGW" == "true" ] && [ "$CI" == "true" ]; then
                (mintty --title "$TEST_NAME" --hold always --exec cat "$TEST_LOG")&
            else
                echo -n "::group::"
                cat "$TEST_LOG"
                echo "::endgroup::"
            fi
        fi
        if [ -n "$TEST_ERR" ] && [ -f "$TEST_ERR" ]; then
            echo "::group::Print $TEST_ERR"
            cat "$TEST_ERR"
            echo "::endgroup::"
        fi
        if [ "$IS_LINUX" == "true" ] && [ "$TEST_APPTYPE" == "cui" ]; then
            echo "::group::Run '$TEST_NAME' sample in docker"
            printf '=%.0s' {1..40}
            TEST_DOCKER=/frozen/$(basename "$TEST_NAME")
            DOCKER_APP=$(which podman)
            if [ -z "$DOCKER_APP" ]; then
                DOCKER_APP=$(which docker)
            fi
            if [ -n "$DOCKER_APP" ]; then
                $DOCKER_APP run --rm -t \
                    -v "$PWD":/frozen ubuntu:20.04 "$TEST_DOCKER"
            else
                echo "INFO: Neither podman nor docker installed."
            fi
            printf '=%.0s' {1..40}
            echo "::endgroup::"
        fi
        echo "::group::Prepare to run the next '$TEST_SAMPLE' sample"
        count=$(( count + 1 ))
    done < <($BASE_PYTHON "$CI_DIR/build_run.py" "$TEST_SAMPLE" --directory="$BUILD_DIR")
    popd >/dev/null || true
done
kill_xvfb "$PY_PLATFORM"
echo "status=$TEST_EXITCODE_FAIL"
echo "::endgroup::"
# shellcheck disable=2086
exit $TEST_EXITCODE_FAIL
