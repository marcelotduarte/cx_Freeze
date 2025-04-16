#!/bin/bash

# Install/update uv
if ! [ "$CI" == "true" ]; then
    if which uv &>/dev/null; then
        uv self -q update
    else
        curl -LsSf https://astral.sh/uv/install.sh | \
        env UV_INSTALL_DIR="$HOME/bin" INSTALLER_NO_MODIFY_PATH=1 sh
    fi
fi
