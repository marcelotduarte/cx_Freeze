#!/bin/bash

if [ -z "$1" ] ; then
	echo "Usage: $0 sample"
	echo "Where:"
	echo "  sample is the name in samples directory (e.g. cryptography)"
	exit 1
fi
TEST_SAMPLE=$1
MANYLINUX_X86_64_IMAGE="quay.io/pypa/manylinux2014_x86_64:latest"

set -e -u -x

# Get script directory (without using /usr/bin/realpath)
_CI_DIR=$(dirname "${BASH_SOURCE[0]}")
CI_DIR=$(cd "$_CI_DIR" && pwd)
TOP_DIR=$(cd "$CI_DIR/.." && pwd)

# Generate the script to build and run the test
SAMPLE_DIR="$TOP_DIR/samples/$TEST_SAMPLE"
mkdir -p "$SAMPLE_DIR/build"
cat <<EOF >"$SAMPLE_DIR/build/build-test-$TEST_SAMPLE.sh"
#!/bin/bash
cd /io/samples/"$TEST_SAMPLE"
for PYBIN in /opt/python/cp*/bin ; do
    PYTHON=\${PYBIN}/python
    PY_COMMAND="import sysconfig; print(sysconfig.get_python_version())"
    PY_VERSION=\$(\${PYTHON} -c "\${PY_COMMAND}")
    BUILD_ENV=/io/build/venv-\"$TEST_SAMPLE\"-\${PY_VERSION}
    echo "Freeze sample: "$TEST_SAMPLE""
    echo "Python from: \${PYBIN}"
    echo "Platform: ${POLICY}_${PLATFORM}"
    echo "Python version: \${PY_VERSION}"
    "\${PYTHON}" -m venv --system-site-packages \${BUILD_ENV}
    source \${BUILD_ENV}/bin/activate
    pip install -U pip
    pip uninstall -y cx_Freeze || true
    pip install -f /io/wheelhouse cx_Freeze --no-index
    /io/ci/build-test-one.sh \"$TEST_SAMPLE\"
    deactivate || true
done
chown -R \$USER_ID:\$GROUP_ID build/exe.linux-${PLATFORM}-*
EOF
chmod +x "$SAMPLE_DIR/build/build-test-$TEST_SAMPLE.sh"

# Build and run the test in the manylinux2014 container
docker run --rm -ti -v "$TOP_DIR":/io \
	$MANYLINUX_X86_64_IMAGE \
	"/io/samples/$TEST_SAMPLE/build/build-test-$TEST_SAMPLE.sh"

# The built test in manylinux2014 container should run in a different container
echo "Run sample isolated in a docker: \"$TEST_SAMPLE\""
echo "Platform: ubuntu:16.04 ${PLATFORM}"
PY_PLATFORM=$(python -c "import sysconfig; print(sysconfig.get_platform())")
for PY_VERSION in '3.7' '3.8' '3.9' '3.10' '3.11'; do
    BUILD_DIR="$SAMPLE_DIR/build/exe.${PY_PLATFORM}-${PY_VERSION}"
    count=0
    TEST_NAME=$(python "$CI_DIR/build_test.py" "$TEST_SAMPLE" --get-app=${count})
    until [ -z "$TEST_NAME" ] ; do
        if [[ "$TEST_NAME" == gui:* ]] || [[ "$TEST_NAME" == svc:* ]] ; then
            TEST_NAME=${TEST_NAME:4}
        fi
        if [ -f "$BUILD_DIR/$TEST_NAME" ] ; then
            docker run --rm \
                -v "$BUILD_DIR":/frozen \
                ubuntu:16.04 /frozen/"$TEST_NAME"
            if [ "$TEST_SAMPLE" == "simple" ] ; then
                echo "test - rename the executable"
                cp "$BUILD_DIR/hello" "$BUILD_DIR/Test_Hello"
                docker run --rm \
                    -v "$BUILD_DIR":/frozen \
                    ubuntu:16.04 /frozen/Test_Hello ação ótica côncavo peña
            fi
        fi
        count=$(( count + 1 ))
        TEST_NAME=$(python "$CI_DIR/build_test.py" "$TEST_SAMPLE" --get-app=${count})
    done
done
