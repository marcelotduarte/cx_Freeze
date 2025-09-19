#!/bin/bash

INSTALL_DIR="$HOME/bin"
mkdir -p "$INSTALL_DIR"

if which python &>/dev/null; then
    PY_PLATFORM=$(python -c "import sysconfig; print(sysconfig.get_platform(), end='')")
else
    PY_PLATFORM=""
fi

IS_CONDA=$([ -n "$CONDA_EXE" ] && echo 1)
IS_LINUX=$([[ $PY_PLATFORM == linux* ]] && echo 1)
IS_MINGW=$([[ $PY_PLATFORM == mingw* ]] && echo 1)

# For Linux
PYTHON_FOR_DEV="3.12"

# Usage
if [ -n "$1" ] && [ "$1" == "--help" ]; then
    echo "Usage:"
    echo "$0 [--tests]"
    echo "Where:"
    echo "  --dev   Install additional packages for development."
    echo "  --tests Install additional packages to run 'pytest'."
    exit 1
fi

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
# Install/update uv and dev tools
if [ "$IS_CONDA" == "1" ]; then
    SYS_PLATFORM=$(python -c "import sys; print(sys.platform, end='')")
    # Packages to install
    pkgs=("uv" "python-build")

    # Dependencies of the project
    if [ -f requirements.txt ]; then
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

    # Install libmamba-solver and use it to speed up packages install
    echo "Update conda to use libmamba-solver"
    $CONDA_EXE clean --index-cache --logfiles --quiet --yes
    $CONDA_EXE update -n base conda --quiet --yes
    $CONDA_EXE install -n base conda-libmamba-solver --quiet --yes
    $CONDA_EXE config --set solver libmamba
    echo "Install packages"
    echo "${pkgs[@]}"
    $CONDA_EXE install -c conda-forge "${pkgs[@]}" -S -q -y
elif [ "$IS_MINGW" == "1" ]; then
    # Packages to install
    pkgs=("$MINGW_PACKAGE_PREFIX-uv" "$MINGW_PACKAGE_PREFIX-python-build")

    # Dependencies of the project
    if [ -f requirements.txt ]; then
        while read -r line; do
            if [[ $line != *sys_platform* ]] || \
               [[ $line == *sys_platform*==*win32* ]]; then
                name=$(echo "$line" | awk -F '[><=]+' '{ print $1 }')
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
    if [ "$CI" == "1" ]; then
        if ! which uv &>/dev/null; then
            echo "error: Please install uv"
            exit 1
        fi
    else
        if which uv &>/dev/null; then
            uv self -q update
        else
            curl -LsSf https://astral.sh/uv/install.sh | \
            env UV_INSTALL_DIR="$INSTALL_DIR" sh
        fi
    fi

    # Dependencies of the project
    echo "Install packages"
    if [ "$INSTALL_TESTS" == "1" ]; then
        # including pytest and dependencies
        uv pip install --extra tests --upgrade -r pyproject.toml
    else
        uv pip install --upgrade -r pyproject.toml
    fi
fi

# Install dev tools
if [ "$INSTALL_DEV" == "1" ]; then
    if [ "$IS_LINUX" == "1" ] || [ "$IS_MINGW" == "1" ] || \
       [ "$IS_CONDA" == "1" ]; then
        if [ -f requirements-dev.txt ]; then
            while read -r line; do
                name=$(echo "$line" | awk -F '[><=]+' '{ print $1 }')
                filename=$INSTALL_DIR/$name
                echo "Create $filename"
                echo "#!/bin/bash"> "$filename"
                if [ "$name" == "bump-my-version" ]; then
                    echo "uvx -p $PYTHON_FOR_DEV -w \"click<8.3.0\" \"$line\" \$@">> "$filename"
                else
                    echo "uvx -p $PYTHON_FOR_DEV \"$line\" \$@">> "$filename"
                fi
                chmod +x "$filename"
            done < requirements-dev.txt
        fi
    else
        # macOS and Windows
        uv pip install --extra dev --upgrade -r pyproject.toml
        uv pip install --upgrade build
    fi
fi
echo "::endgroup::"
