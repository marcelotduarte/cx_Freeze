#!/bin/bash

# Get script directory (without using /usr/bin/realpath)
CI_DIR=$(cd `dirname "${BASH_SOURCE[0]}"` && pwd)
# Install/update uv
$CI_DIR/install-uv.sh

make -C doc html
