#!/bin/bash

# Usage
if [ -n "$1" ] && [ "$1" == "--help" ]; then
    echo "Usage:"
    echo "$0 [--tests]"
    echo "Where:"
    echo "  --dev   Install additional packages for development."
    echo "  --tests Install additional packages to run 'pytest'."
    exit 1
fi

# Detect environment
IS_CONDA="0"
IS_MINGW="0"
IS_WINDOWS="0"
if [ -n "$CONDA_EXE" ]; then
    IS_CONDA="1"
elif [ -n "$MINGW_PACKAGE_PREFIX" ]; then
    IS_MINGW="1"
elif which python &>/dev/null; then
    PY_PLATFORM=$(python -c "import sysconfig; print(sysconfig.get_platform(), end='')")
    IS_WINDOWS=$([[ $PY_PLATFORM == win* ]] && echo "1")
else
    echo "error: Python is required."
    exit 1
fi

# Install/update dev tools (including uv if required)
INSTALL_DIR="$HOME/bin"
mkdir -p "$INSTALL_DIR"

INSTALL_DEV=""
INSTALL_TESTS=""
while [ -n "$1" ]; do
    if [ "$1" == "--dev" ]; then
        INSTALL_DEV="1"
    elif [ "$1" == "--tests" ]; then
        INSTALL_TESTS="1"
    else
        echo "WARNING: invalid option '$1'"
    fi
    shift
done

echo "::group::Install dependencies and build tools"
if [ "$IS_CONDA" == "1" ]; then
    # Install libmamba-solver and use it to speed up packages installation
    echo "Update conda to use libmamba-solver"
    $CONDA_EXE clean --index-cache --logfiles --quiet --yes
    $CONDA_EXE update -n base conda --quiet --yes
    $CONDA_EXE install -n base conda-libmamba-solver --quiet --yes
    $CONDA_EXE config --set solver libmamba
    if ! which python &>/dev/null; then
        $CONDA_EXE install -c conda-forge python -S -q -y
    fi
    # Packages to install
    pkgs=("python-build")

    # Dependencies of the project
    if [ -f requirements.txt ]; then
        SYS_PLATFORM=$(python -c "import sys; print(sys.platform, end='')")
        while read -r line; do
            if [[ $line != *sys_platform* ]] || \
               [[ $line == *sys_platform*==*${SYS_PLATFORM}* ]]; then
                name=$(echo "$line" | awk -F '[><=]+' '{ print $1 }')
                if [ "$name" == "cx-logging" ]; then name="cx_logging"; fi
                if [ "$name" == "lief" ]; then name="py-lief"; fi
                if ! printf '%s\0' "${pkgs[@]}" | grep -Fxqz -- "$name"; then
                    pkgs+=("$name")
                fi
            fi
        done < requirements.txt
    fi

    # pytest and dependencies
    if [ "$INSTALL_TESTS" == "1" ] && [ -f tests/requirements.txt ]; then
        while read -r line; do
            name=$(echo "$line" | awk -F '[><=]+' '{ print $1 }')
            pkgs+=("$name")
        done < tests/requirements.txt
    fi

    echo "Install packages"
    echo "${pkgs[@]}"
    $CONDA_EXE install -c conda-forge "${pkgs[@]}" -S -q -y
elif [ "$IS_MINGW" == "1" ]; then
    # Packages to install
    pkgs=("$MINGW_PACKAGE_PREFIX-python-build")
    if ! which python &>/dev/null; then
        pkgs+=("$MINGW_PACKAGE_PREFIX-python")
    fi

    # Dependencies of the project
    if [ -f requirements.txt ]; then
        while read -r line; do
            if [[ $line != *sys_platform* ]] || \
               [[ $line == *sys_platform*==*win32* ]]; then
                name=$(echo "$line" | awk -F '[><=]+' '{ print $1 }')
                if [ "$name" == "python-msilib" ]; then name="msilib"; fi
                if ! printf '%s\0' "${pkgs[@]}" | grep -Fxqz -- "$name"; then
                    pkgs+=("$MINGW_PACKAGE_PREFIX-python-$name")
                fi
            fi
        done < requirements.txt
    fi

    # pytest and dependencies
    if [ "$INSTALL_TESTS" == "1" ] && [ -f tests/requirements.txt ]; then
        while read -r line; do
            name=$(echo "$line" | awk -F '[><=]+' '{ print $1 }')
            pkgs+=("$MINGW_PACKAGE_PREFIX-python-$name")
        done < tests/requirements.txt
    fi

    echo "Install packages"
    pacman --needed --noconfirm --quiet -S "${pkgs[@]}"
else
    if [ "$CI" == "true" ]; then
        if [ "$IS_WINDOWS" == "1" ]; then
            export UV_LINK_MODE=copy
        fi
    elif which uv &>/dev/null; then
        uv self -q update
    fi
    if ! which uv &>/dev/null; then
        curl -LsSf https://astral.sh/uv/install.sh | \
            env UV_INSTALL_DIR="$INSTALL_DIR" sh
    fi

    # Lief is not available for Python 3.13t and 3.14t
    PY_VERSION=$(python -c "import sysconfig; print(sysconfig.get_python_version(), end='')")
    PY_ABI_THREAD=$(python -c "import sysconfig; print(sysconfig.get_config_var('abi_thread') or '', end='')")
    PY_VER_ABI="$PY_VERSION$PY_ABI_THREAD"
    if [ "$IS_WINDOWS" == "1" ] && \
       { [ "$PY_VER_ABI" == "3.13t" ] || [ "$PY_VER_ABI" == "3.14t" ]; }; then
        # Packages to install
        pkgs=()

        # Dependencies of the project
        if [ -f requirements.txt ]; then
            while read -r line; do
                if [[ $line != *sys_platform* ]] || \
                   [[ $line == *sys_platform*==*win32* ]]; then
                    name=$(echo "$line" | awk -F '[><=]+' '{ print $1 }')
                    if [ "$name" == "lief" ]; then continue; fi
                    if [ "$name" == "tomli" ]; then continue; fi
                    name_and_version=$(echo "$line" | awk '{ print $1 }')
                    pkgs+=("$name_and_version")
                fi
            done < requirements.txt
        fi

        # pytest and dependencies
        if [ "$INSTALL_TESTS" == "1" ] && [ -f tests/requirements.txt ]; then
            while read -r line; do
                name=$(echo "$line" | awk -F '[><=]+' '{ print $1 }')
                pkgs+=("$name")
            done < tests/requirements.txt
        fi

        echo "Install packages"
        uv pip install --upgrade "${pkgs[@]}"

    else
        # Dependencies of the project
        echo "Install packages"
        if [ "$INSTALL_TESTS" == "1" ]; then
            # including pytest and dependencies
            uv pip install --upgrade -r pyproject.toml --group tests
        else
            uv pip install --upgrade -r pyproject.toml
        fi
    fi
fi

# Install dev tools
if [ "$INSTALL_DEV" == "1" ]; then
    if [ -f requirements-dev.txt ]; then
        PY_VERSION=$(python -c "import sysconfig; print(sysconfig.get_python_version(), end='')")
        PY_ABI_THREAD=$(python -c "import sysconfig; print(sysconfig.get_config_var('abi_thread') or '', end='')")
        PY_VER_ABI="$PY_VERSION$PY_ABI_THREAD"
        while read -r line; do
            name=$(echo "$line" | awk -F '[><=]+' '{ print $1 }')
            filename=$INSTALL_DIR/$name
            echo "Create $filename"
            echo "#!/bin/sh"> "$filename"
            echo "uvx -p $PY_VER_ABI \"$line\" \$@">> "$filename"
            chmod +x "$filename"
        done < requirements-dev.txt
    fi
fi
echo "::endgroup::"
