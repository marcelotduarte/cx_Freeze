#!/bin/bash

# Get script directory (without using /usr/bin/realpath)
_CI_DIR=$(dirname "${BASH_SOURCE[0]}")
CI_DIR=$(cd "$_CI_DIR" && pwd)

# Python information (platform and version)
if ! which uv &>/dev/null; then
    # Install/update uv
    "$CI_DIR/install-tools.sh" --dev
fi

# Usage
_usage () {
    echo "Usage:"
    echo "$0 <major|minor|patch|dev|stable>"
    echo "Based on:"
    echo "  https://docs.astral.sh/uv/reference/cli/#uv-version--bump"
    echo "Also can be used as:"
    echo "$0 <major-dev|minor-dev|patch-dev|build-dev>"
}

if [ -z "$1" ] || [ "$1" == "--help" ]; then
    _usage
    exit 1
fi

echo "::group::Bump new version"
VERSION=$(uv version --short)
if [ "$1" == "major" ] || [ "$1" == "minor" ] || [ "$1" == "patch" ]; then
    uv version --no-sync --bump "$1"
    exit_value=$?
elif [ "$1" == "stable" ]; then
    uv version --no-sync --bump stable
    exit_value=$?
    if [ $exit_value != 0 ]; then
        echo "You must create a <dev> release first."
        exit $exit_value
    fi
elif [ "$1" == "dev" ]; then
    if (echo "$VERSION" | grep -q "\.dev"); then
        uv version --no-sync --bump dev
    else
        uv version --no-sync --bump patch --bump dev=0
    fi
    exit_value=$?
elif [ "$1" == "build-dev" ]; then
    SOURCE_DATE_EPOCH=$(git log -1 --pretty=%ct)
    if (echo "$VERSION" | grep -q "\.dev"); then
        uv version --no-sync --bump dev="$SOURCE_DATE_EPOCH"
    else
        uv version --no-sync --bump patch --bump dev="$SOURCE_DATE_EPOCH"
    fi
    exit_value=$?
elif [ "$1" == "major-dev" ] || [ "$1" == "minor-dev" ] || [ "$1" == "patch-dev" ]; then
    if (echo "$VERSION" | grep -q "\.dev"); then
        echo "error: to increase an <dev> version, use <dev> option or <build-dev> option."
        exit 1
    fi
    if [ "$1" == "major-dev" ]; then
        uv version --no-sync --bump major --bump dev=0
    elif [ "$1" == "minor-dev" ]; then
        uv version --no-sync --bump minor --bump dev=0
    elif [ "$1" == "patch-dev" ]; then
        uv version --no-sync --bump patch --bump dev=0
    fi
    exit_value=$?
else
    echo "error: invalid option: $1"
    exit 1
fi
if [ $exit_value != 0 ]; then
    exit $exit_value
fi
NEW_VERSION=$(uv version --short)
if ! (git config --get user.email | grep -q "@"); then
    git config user.name "Marcelo Duarte"
    git config user.email marcelotduarte@users.noreply.github.com
fi
if (git branch --show-current | grep -q "main"); then
    git checkout -B release main
fi
git commit -m "Bump version: ${VERSION} → ${NEW_VERSION} [ci skip]" -a
git log -1
if ! [ "$CI" == "true" ]; then
    git push origin "$(git branch --show-current)"
    if ! (echo "$NEW_VERSION" | grep -q "\.dev"); then
        git tag -s "$NEW_VERSION" -m "Bump version: ${NEW_VERSION}"
        git push origin "$(git branch --show-current)" --tags
    fi
fi
echo "::endgroup::"
