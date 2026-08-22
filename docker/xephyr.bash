#!/bin/bash
# Start a nested Xephyr X11 server (if not already running) for GUI apps like rviz2.
#
# rviz2/Gazebo use Ogre's legacy GLX window-embedding path, which races against
# XWayland's window realization and reliably fails with "Invalid parentWindowHandle
# (wrong server or screen)". Xephyr provides a real, synchronous X11 server (as a
# window on the host desktop) that does not have this race.

XEPHYR_DISPLAY=":10"
export XEPHYR_AUTH_FILE="${HOME}/.xephyr_auth"

if ! xdpyinfo -display "${XEPHYR_DISPLAY}" &> /dev/null
then
    touch "${XEPHYR_AUTH_FILE}"
    xauth -f "${XEPHYR_AUTH_FILE}" generate "${XEPHYR_DISPLAY}" . trusted &> /dev/null

    # Xephyr is itself a client of the host's real display, so it needs the host's
    # own DISPLAY/XAUTHORITY (unchanged); -auth only governs its own nested display.
    Xephyr "${XEPHYR_DISPLAY}" \
        -auth "${XEPHYR_AUTH_FILE}" \
        -br -screen 1920x1080 -resizeable -glamor \
        &> /tmp/xephyr.log &
    disown

    # Wait for Xephyr to come up before returning.
    for i in $(seq 1 20)
    do
        xdpyinfo -display "${XEPHYR_DISPLAY}" &> /dev/null && break
        sleep 0.2
    done
fi

export XEPHYR_DISPLAY
