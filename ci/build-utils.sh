#!/bin/bash

install_docker_or_podman () {
    local platform=$1
    if [[ $platform == linux* ]] ; then
        if ! which docker &>/dev/null ; then
            if ! which podman &>/dev/null ; then
                echo "INFO: Install the podman."
                sudo apt-get install -y podman
            else
                echo "INFO: podman already installed."
            fi
            if ! alias docker &>/dev/null ; then
                alias docker=podman
            fi
        else
            echo "INFO: docker already installed."
        fi
    fi
}

install_screen_capture () {
    local platform=$1
    if [[ $platform == mingw* ]] || [[ $platform == win* ]] ; then
        echo "INFO: Install screencapture in Windows/MSYS2"
        mkdir -p $HOME/bin
        if ! [ -e $HOME/bin/screencapture.exe ] ; then
            pushd $HOME/bin
            #curl https://raw.githubusercontent.com/npocmaka/batch.scripts/master/hybrids/.net/c/screenCapture.bat -O screencapture.bat
            cp $CI_DIR/screencapture.bat screencapture.bat
            cmd //c screencapture.bat
            popd
        fi
    elif [[ $platform == linux* ]] ; then
        echo "INFO: Install screencapture (imagemagick) in Linux"
        if ! (dpkg -l | grep -q imagemagick-6.q16) ; then
            sudo apt-get install -y imagemagick-6.q16
        fi
        if ! [ "$CI" == "true" ] ; then
            echo "INFO: Install screencapture (gnome-screenshot) in Linux"
            if ! which gnome-screenshot &>/dev/null ; then
                sudo apt-get install -y gnome-screenshot
            fi
        fi
    fi
}

install_x11_tools () {
    local platform=$1
    if [[ $platform == linux* ]] ; then
        # https://doc.qt.io/qt-6/linux-requirements.html
        if ! (dpkg -l | grep -q libx11-xcb-dev) ; then
            sudo apt-get install -y \
                libfontconfig1-dev \
                libfreetype6-dev \
                libx11-dev \
                libx11-xcb-dev \
                libxext-dev \
                libxfixes-dev \
                libxi-dev \
                libxrender-dev \
                libxcb1-dev \
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
                libxcb-xinerama0-dev \
                libxkbcommon-dev \
                libxkbcommon-x11-dev
                #dmz-cursor-theme light-themes shared-mime-info

        fi
        if ! (dpkg -l | grep -q gstreamer1.0-libav) ; then
            sudo apt-get install -y \
                ffmpeg gstreamer1.0-libav gstreamer1.0-plugins-{ugly,bad,good}
        fi
        # https://doc.qt.io/qt-6/linux.html#requirements-for-development-host
        if ! (dpkg -l | grep -q libgl1-mesa-dev) ; then
            sudo apt-get install -y libgl1-mesa-dev
        fi
        # wxWidgets
        if ! (dpkg -l | grep -q libsdl2-2.0-0) ; then
            sudo apt-get install -y libsdl2-2.0-0
        fi
        # qt?
        if ! (dpkg -l | grep -q ubuntu-restricted-extras) ; then
            sudo apt-get install -y --install-recommends fonts-ubuntu \
            ubuntu-restricted-extras xfonts-75dpi xfonts-base \
            xfonts-encodings xfonts-scalable xfonts-utils
        fi
        #if ! (dpkg -l | grep -q libqt5gui5) ; then
        #    sudo apt-get install -y libqt5gui5 libqt5svg5
        #fi
        #if ! (dpkg -l | grep -q libqt6pdf6) ; then
        #    sudo apt-get install -y libqt6pdf6
        #fi
    fi
}

install_xvfb () {
    local platform=$1
    if [[ $platform == linux* ]] && [ "$CI" == "true" ] ; then
        if ! (dpkg -l | grep -q xvfb) ; then
            echo "INFO: Install the Xvfb as virtual display."
            sudo apt-get install -y xvfb
        else
            echo "INFO: Xvfb already installed."
        fi
    fi
}

start_xvfb () {
    local platform=$1
    if [[ $platform == linux* ]] && [ "$CI" == "true" ] ; then
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
    if [[ $platform == linux* ]] && [ "$CI" == "true" ] ; then
        local xvfb_pid=`cat /tmp/custom_xvfb_99.pid`
        if [ "$xvfb_pid" != "" ]; then
            echo "INFO: Killing the following xvfb process: $xvfb_pid"
            kill $xvfb_pid
        else
            echo "WARING: No xvfb processes to kill"
        fi
    fi
}

cx_freeze_version () {
    local python_exe=$1
    local python_cmd="import cx_Freeze; print(cx_Freeze.__version__)"
    echo $($python_exe -c "${python_cmd}" 2>/dev/null)
}
