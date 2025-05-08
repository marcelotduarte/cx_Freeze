#!/bin/bash

INSTALL_DIR="$HOME/bin"
PY_VERSION=3.12

mkdir -p "$INSTALL_DIR"

if which python &>/dev/null; then
    PY_PLATFORM=$(python -c "import sysconfig; print(sysconfig.get_platform(), end='')")
else
    PY_PLATFORM=""
fi

echo "::group::Install dependencies and build tools"
# Install/update uv and dev tools
if [[ $PY_PLATFORM == mingw* ]]; then
    PY_VERSION=$(python -c "import sysconfig; print(sysconfig.get_python_version(), end='')")

    # Packages to install
    pkgs=("$MINGW_PACKAGE_PREFIX-uv" "$MINGW_PACKAGE_PREFIX-python-build")

    # Dependencies of cx_Freeze
    while read -r line; do
        if [[ $line != *sys_platform* ]] || \
           [[ $line == *sys_platform*==*win32* ]]; then
            name=$(echo $line | awk -F '[><=]+' '{ print $1 }')
            if [ "$name" == "cx_Logging" ]; then name="cx-logging"; fi
            pkgs+=("$MINGW_PACKAGE_PREFIX-python-$name")
        fi
    done < requirements.txt

    # pytest and dependencies
    while read -r line; do
        name=$(echo $line | awk -F '[><=]+' '{ print $1 }')
        pkgs+=("$MINGW_PACKAGE_PREFIX-python-$name")
    done < tests/requirements.txt

    pacman --needed --noconfirm --quiet -S ${pkgs[@]}
else
    if [ "$CI" == "true" ]; then
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
    uv pip install --extra tests --upgrade -r pyproject.toml
fi

# Install dev tools
while read -r line; do
    name=$(echo $line | awk -F '[><=]+' '{ print $1 }')
    if [[ $PY_PLATFORM != mingw* ]] || [ "$name" != "cibuildwheel" ]; then
        filename=$INSTALL_DIR/$name
        echo "Create $filename"
        echo "#!/bin/bash"> $filename
        echo "uvx -p $PY_VERSION \"$line\" \$@">> $filename
        chmod +x $filename
    fi
done < requirements-dev.txt
echo "::endgroup::"
