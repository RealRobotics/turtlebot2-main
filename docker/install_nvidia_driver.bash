#!/bin/dash

DISTRO=ubuntu2604
# The versions chosen are the stable ones (least likely to fail) and work on this version of Ubuntu.
DRIVER_VERSION=580
CUDA_VERSION=13-1

# Install the NVIDIA driver if it is not already installed.
# From: https://docs.nvidia.com/datacenter/tesla/driver-installation-guide/latest/ubuntu.html
sudo apt update
sudo apt install linux-headers-$(uname -r)

wget https://developer.download.nvidia.com/compute/cuda/repos/$DISTRO/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb

sudo apt install nvidia-driver-${DRIVER_VERSION}-open nvidia-dkms-${DRIVER_VERSION}-open
echo "Driver installed."

# Install CUDA Toolkit.  Based on:
# https://docs.nvidia.com/cuda/cuda-installation-guide-linux/#network-repo-installation-for-ubuntu
sudo apt install -y cuda-toolkit-${CUDA_VERSION}

# Post installation steps
# Mandatory
CUDA_DIR=/usr/local/cuda-$(echo ${CUDA_VERSION} | tr '-' '.')
export PATH=${PATH}:${CUDA_DIR}/bin
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${CUDA_DIR}/lib64


echo "NVidia driver installation complete.  Please reboot your computer to ensure the driver is loaded."
exit 0
