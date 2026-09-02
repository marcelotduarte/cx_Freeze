#!/bin/bash

get_python () {
    local PYTHON=""
    if [ -n "$CONDA_EXE" ]; then
        if [ "$OSTYPE" == "cygwin" ] || [ "$OSTYPE" == "msys" ]; then
            PYTHON=$(cygpath -u "$CONDA_PREFIX/python.exe")
        else
            PYTHON="$CONDA_PREFIX/bin/python"
        fi
    elif which python &>/dev/null; then
        PYTHON=python
    elif which python3 &>/dev/null; then
        PYTHON=python3
    fi
    if [ -n "$PYTHON" ]; then
        local platform
        platform=$($PYTHON -c "import sysconfig; print(sysconfig.get_platform(), end='')")
        if [[ $platform == macos* ]]; then
            local py_version
            py_version=$($PYTHON -c "import sysconfig; print(sysconfig.get_python_version(), end='')")
            if ! [[ $py_version == *3.* ]]; then
                if [ "$CI" == "true" ] && which python3 &>/dev/null; then
                    PYTHON=python3
                else
                    PYTHON=""
                fi
            fi
            if [ -z "$PYTHON" ] && which brew &>/dev/null; then
                if ! [ -d "$(brew --prefix python@3.10)" ]; then
                    brew install python@3.10
                fi
                PYTHON=$(brew --prefix python@3.10)/bin/python3.10
            fi
        fi
    fi
    if [[ $PYTHON == python* ]]; then
        PYTHON=$(which "$PYTHON")
    fi
    echo "$PYTHON"
}

get_python_error () {
    local PYTHON=""
    if [ -n "$CONDA_PYTHON_EXE" ]; then
        PYTHON=$CONDA_PYTHON_EXE
    elif which python &>/dev/null; then
        PYTHON=python
    elif which python3 &>/dev/null; then
        PYTHON=python3
    fi
    if [ -n "$PYTHON" ]; then
        local platform
        platform=$($PYTHON -c "import sysconfig; print(sysconfig.get_platform(), end='')")
        local py_version
        py_version=$($PYTHON -c "import sysconfig; print(sysconfig.get_python_version(), end='')")
        if [[ $platform == macos* ]] && ! [[ $py_version == *3.* ]]; then
            echo "You can use homebrew to install python."
            echo "sudo rm -rf /Library/Developer/CommandLineTools"
            echo "sudo xcode-select --install"
            # shellcheck disable=2016
            echo '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
            echo "brew install python@3.10"
            return
        fi
    fi
    echo "ERROR: python3 not found!"
}

install_docker_or_podman () {
    local platform=$1
    if [[ $MACHTYPE == *-redhat-* ]]; then
        return
    fi
    if [[ $platform == linux* ]]; then
        if ! which docker &>/dev/null; then
            if ! which podman &>/dev/null; then
                echo "INFO: Install the podman."
                sudo apt-get install -q -y --no-upgrade podman
            else
                echo "INFO: podman already installed."
            fi
        else
            echo "INFO: docker already installed."
        fi
    fi
}

install_screen_capture () {
    local platform=$1
    if [[ $MACHTYPE == *-redhat-* ]]; then
        return
    fi
    if [[ $platform == cygwin* ]] || [[ $platform == mingw* ]] || [[ $platform == win* ]]; then
        echo "INFO: Install screencapture in Windows/MSYS2"
        mkdir -p "$HOME/bin"
        if ! [ -e "$HOME/bin/screencapture.exe" ]; then
            pushd "$HOME/bin" >/dev/null || return
            #curl https://raw.githubusercontent.com/npocmaka/batch.scripts/master/hybrids/.net/c/screenCapture.bat -O screencapture.bat
            cp "$CI_DIR/screencapture.bat" screencapture.bat
            cmd //c screencapture.bat
            popd >/dev/null || return
        fi
    elif [[ $platform == linux* ]]; then
        echo "INFO: Install screencapture (imagemagick) in Linux"
        if ! (dpkg -l --no-pager | grep -q imagemagick-6.q16); then
            sudo apt-get install -q -y --no-upgrade imagemagick-6.q16
        fi
        if ! [ "$CI" == "true" ]; then
            echo "INFO: Install screencapture (gnome-screenshot) in Linux"
            if ! which gnome-screenshot &>/dev/null; then
                sudo apt-get install -q -y --no-upgrade gnome-screenshot
            fi
        fi
    fi
}

install_x11_tools () {
    local platform=$1
    if [[ $MACHTYPE == *-redhat-* ]]; then
        return
    fi
    if [[ $platform == linux* ]]; then
        if [ "$CI" == "true" ]; then
            sudo apt-get update && sudo apt-get upgrade -y
        fi
        # https://doc.qt.io/qt-6/linux-requirements.html
        if ! (dpkg -l --no-pager | grep -q libx11-xcb-dev); then
            sudo apt-get install -q -y --no-upgrade \
                libfontconfig1-dev \
                libfreetype6-dev \
                libx11-dev \
                libx11-xcb-dev \
                libxext-dev \
                libxfixes-dev \
                libxi-dev \
                libxrender-dev \
                libxcb1-dev \
                libxcb-cursor-dev \
                libxcb-glx0-dev \
                libxcb-keysyms1-dev \
                libxcb-image0-dev \
                libxcb-shm0-dev \
                libxcb-icccm4-dev \
                libxcb-sync-dev \
                libxcb-xfixes0-dev \
                libxcb-shape0-dev \
                libxcb-randr0-dev \
                libxcb-render-util0-dev \
                libxcb-util-dev \
                libxcb-xinerama0-dev \
                libxcb-xkb-dev \
                libxkbcommon-dev \
                libxkbcommon-x11-dev
                #dmz-cursor-theme light-themes shared-mime-info

        fi
        if ! (dpkg -l --no-pager | grep -q gstreamer1.0-libav); then
            sudo apt-get install -q -y --no-upgrade \
                ffmpeg gstreamer1.0-libav gstreamer1.0-plugins-{ugly,bad,good}
        fi
        # https://doc.qt.io/qt-6/linux.html#requirements-for-development-host
        if ! (dpkg -l --no-pager | grep -q libgl1-mesa-dev); then
            sudo apt-get install -q -y --no-upgrade libgl1-mesa-dev
        fi
        # wxWidgets
        if ! (dpkg -l --no-pager | grep -q libsdl2-2.0-0); then
            sudo apt-get install -q -y --no-upgrade libsdl2-2.0-0
        fi
        if ! (dpkg -l --no-pager | grep -q libnotify4); then
            sudo apt-get install -q -y --no-upgrade libnotify4
        fi
        # qt?
        if ! (dpkg -l --no-pager | grep -q ubuntu-restricted-extras); then
            sudo apt-get install -q -y --no-upgrade fonts-ubuntu \
                ubuntu-restricted-extras xfonts-75dpi xfonts-base \
                xfonts-encodings xfonts-scalable xfonts-utils
        fi
    fi
}

install_xvfb () {
    local platform=$1
    if [[ $platform == linux* ]] && [ "$CI" == "true" ]; then
        if ! (dpkg -l --no-pager | grep -q xvfb); then
            echo "INFO: Install the Xvfb as virtual display."
            sudo apt-get install -q -y --no-upgrade xvfb
        else
            echo "INFO: Xvfb already installed."
        fi
    fi
}

start_xvfb () {
    local platform=$1
    if [[ $platform == linux* ]] && [ "$CI" == "true" ]; then
        echo "INFO: Activate the Xvfb as virtual display in the Github Actions"
        /sbin/start-stop-daemon --start --quiet \
            --pidfile /tmp/custom_xvfb_99.pid --make-pidfile --background \
            --exec /usr/bin/Xvfb -- :99 -screen 0 1024x768x16 \
            -ac +extension GLX +render -noreset -wr
        sleep 10  # wait to start
        export DISPLAY=":99.0"
        # disable opengl for qt webengine
        export QMLSCENE_DEVICE=softwarecontext
    fi
}

kill_xvfb () {
    local platform=$1
    if [[ $platform == linux* ]] && [ "$CI" == "true" ]; then
        local xvfb_pid
        xvfb_pid=$(cat /tmp/custom_xvfb_99.pid)
        if [ "$xvfb_pid" != "" ]; then
            echo "INFO: Killing the following xvfb process: $xvfb_pid"
            kill "$xvfb_pid"
        else
            echo "WARNING: No xvfb processes to kill"
        fi
    fi
}

cx_freeze_version () {
    local python_exe=$1
    local python_cmd="import cx_Freeze; print(cx_Freeze.__version__, end='')"
    $python_exe -c "${python_cmd}" 2>/dev/null
}
