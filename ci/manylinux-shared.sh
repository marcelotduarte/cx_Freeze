#!/bin/bash

if [ -z "${VIRTUAL_ENV}" ] && [ -z "${GITHUB_WORKSPACE}" ] ; then
	echo "Required: use of a virtual environment."
	exit 1
fi

if [ -z "${POLICY}" ] ; then
    export POLICY=manylinux2014
fi
if [ -z "${PLATFORM}" ] ; then
    export PLATFORM=x86_64
fi
if [ -z "${COMMIT_SHA}" ] ; then
    export COMMIT_SHA=latest
fi

# Get script directory (without using /usr/bin/realpath)
_CI_DIR=$(dirname "${BASH_SOURCE[0]}")
CI_DIR=$(cd "$_CI_DIR" && pwd)
TOP_DIR=$(cd "$CI_DIR"/..  && pwd)

# Set manylinux as working directory
if [ -d "$TOP_DIR"/../manylinux ] ; then
	pushd "$TOP_DIR"/../manylinux >/dev/null || exit
elif [ -d "$TOP_DIR"/manylinux ] ; then
	pushd "$TOP_DIR"/manylinux >/dev/null || exit
else
    if [ "${GITHUB_WORKSPACE}" ] ; then
        echo "Please checkout pypa/manylinux"
    else
        pushd "$TOP_DIR"/.. >/dev/null || exit
        PARENT_DIR=$(pwd)
        popd >/dev/null || exit
        echo "Please clone pypa/manylinux at:"
        echo "    \"$TOP_DIR\""
        echo "or"
        echo "    ${PARENT_DIR}"
    fi
	exit 1
fi

echo "Create new branch manylinux-freeze"
git checkout -f main
git checkout -B manylinux-freeze main

echo "Patch the build scripts"
sed -i 's/quay.io\/pypa\/\$/\$/g' build.sh
# remove python 3.5
#sed -i '/RUN manylinux-entrypoint .*3.5/d' docker/Dockerfile
#sed -i '/COPY --from=build_cpython35/d' docker/Dockerfile
# enable shared .so and .lib
SCRIPT=docker/build_scripts/build-cpython.sh
#sed -i 's/--disable-shared --with-ensurepip=no/--enable-shared --enable-optimizations --with-ensurepip=no LDFLAGS=\"-Wl,-rpath,${PREFIX}\/lib\"/g' $SCRIPT
sed -i 's/--disable-shared/--enable-shared/g' $SCRIPT
# shellcheck disable=2016
sed -i 's/NODIST="${MANYLINUX_LDFLAGS}"/NODIST="${MANYLINUX_LDFLAGS} -Wl,-rpath,\${PREFIX}\/lib"/g' $SCRIPT
# enable libpython*.a
sed -i '/find.*.a.*rm -f/d' docker/build_scripts/finalize-python.sh
sed -i 's/XZ_OPT/#XZ_OPT/g' docker/build_scripts/finalize-python.sh
# enable libsqlite3
#sed -i '/rm .*libsqlite3.a/d' docker/build_scripts/build-sqlite3.sh
# enable libffi (cffi and ctypes)
#sed -i 's/\blibffi\b/libffi libffi-devel/g' docker/build_scripts/install-runtime-packages.sh
#sed -i 's/\blibffi6\b/libffi6 libffi-dev/g' docker/build_scripts/install-runtime-packages.sh

echo "Generate requirements"
GEN_REQUIREMENTS_IS_NEEDED=1
function generate_requirements {
    if docker image ls "${POLICY}_${PLATFORM}" -q; then
        # enable importlib-metadata and others in py38+
        echo importlib-metadata>> requirements.in
        echo cffi>> requirements.in
        docker run --rm -v "$PWD":/nox -t "${POLICY}_${PLATFORM}" \
                pipx run nox -f /nox/noxfile.py -s \
                update_python_dependencies update_python_tools
        GEN_REQUIREMENTS_IS_NEEDED=$?
    fi
}

echo "Create docker image"
#generate_requirements
./build.sh

if [ $GEN_REQUIREMENTS_IS_NEEDED != 0 ] ; then
    generate_requirements
    ./build.sh
fi

popd >/dev/null || exit
