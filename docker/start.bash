#!/bin/bash
# Start the docker container.
# set -x

docker_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &>/dev/null && pwd )"
. ${docker_dir}/vars.bash

mkdir -p ${WORKSPACE_DIR}

# Use a nested Xephyr X11 server rather than XWayland directly: Ogre's legacy GLX
# window-embedding code (used by rviz2/Gazebo) races against XWayland's window
# realization and reliably fails with "Invalid parentWindowHandle (wrong server or
# screen)". Xephyr is a real, synchronous X11 server so it doesn't have this race.
. ${docker_dir}/xephyr.bash
host_display="${XEPHYR_DISPLAY}"
host_xauthority="${XEPHYR_AUTH_FILE}"

# Use the NVidia GPU (and its GLX/EGL driver, avoiding Mesa/XWayland DRI3 issues) when available.
gpu_args=()
if command -v nvidia-smi &> /dev/null && nvidia-smi &> /dev/null
then
    # On hybrid-graphics (PRIME) laptops, these force render offload to the NVidia GPU.
    gpu_args+=(
        --gpus=all
        --env="__NV_PRIME_RENDER_OFFLOAD=1"
        --env="__GLX_VENDOR_LIBRARY_NAME=nvidia"
    )
fi

docker container inspect ${CONTAINER_NAME} &> /dev/null
if [ $? == 0 ]
then
    # Container exists.
    if [ "$( docker container inspect -f '{{.State.Status}}' ${CONTAINER_NAME} )" == "running" ]
    then
        # Container is running.
        echo "Container '${CONTAINER_NAME}' is already running."
    else
        # Container exists but is not running.
        docker container start ${CONTAINER_NAME} &> /dev/null
        echo "Container '${CONTAINER_NAME}' started."
    fi
else
    # Container does not exist.
    docker container run \
        --detach \
        --tty \
        --net=host \
        --env="DISPLAY=$host_display" \
        --env ROS_DOMAIN_ID \
        "${gpu_args[@]}" \
        --device-cgroup-rule='c 13:* rmw' \
        --device-cgroup-rule='c 189:* rmw' \
        --device=/dev/dri:/dev/dri \
        --group-add="$(getent group video | cut -d: -f3)" \
        --group-add="$(getent group render | cut -d: -f3)" \
        --volume=/dev/input:/dev/input \
        --volume=/dev/bus/usb:/dev/bus/usb \
        --volume=/tmp/.X11-unix:/tmp/.X11-unix:rw \
        --volume="$host_xauthority:/home/ubuntu/.Xauthority:rw" \
        --env="XAUTHORITY=/home/ubuntu/.Xauthority" \
        --name ${CONTAINER_NAME} \
        --volume ${WORKSPACE_DIR}:/home/ubuntu/ws \
        ${DOCKER_HUB_USER_NAME}/${IMAGE_NAME}:${IMAGE_TAG} &> /dev/null
    if [ $? == 0 ]
    then
        echo "Container '${CONTAINER_NAME}' running."
    else
        echo "Container '${CONTAINER_NAME}' failed."
    fi
fi
