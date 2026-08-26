# Installation and set up on a PC

To control the TurtleBot 2, I decided to use an old laptop, a ThinkPad T410.  The spec of the laptop is:

* CPU: Intel® Core™ i5 M 560  @ 2.67GHz
* Memory: 8 GiB of RAM (7.6 GiB usable)
* Graphics Processor: Mesa Intel® HD Graphics
* HDD: WDC WD1200BEVS-22UST0
* OS: Kubuntu 26.04 LTS

## Installation

Installed Kubuntu 26.04LTS __minimal__ installation with the usual defaults: full HDD being used for the OS, British English locale. 

Installed my Bash scripts:

```bash
mkdir -p git/andyblight
cd git/andyblight/
git clone https://github.com/andyblight/bash_scripts
cd bash_scripts/
./install.sh ubuntu22.04lts/
```

Then setup my Git username and email. Disabled auto updates of everything in `/etc/apt/apt.conf.d/20auto-upgrades` as this device will be treated as a robot controller, not a general use PC.

### Swapfile

Increased the swapfile to 8GB to match the RAM size. 

```bash
sudo swapon --show
sudo swapoff /swapfile 
sudo rm /swapfile 
sudo fallocate -l 8G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
sudo swapon --show
```

### VS Code

```bash
cd /tmp
mv ~/Downloads/code_1.134.0-1787078834_amd64.deb .
sudo apt install ./code_1.134.0-1787078834_amd64.deb 
```

Using `/tmp` allows the installation to complete successfully.  Doing this from your home directory or below causes a sandbox error.

### Firefox

I installeed Firefox using these commands:

```bash
sudo apt update
sudo apt install snapd
sudo snap install firefox
snap warnings
"systemctl enable --now snapd.apparmor"
systemctl enable --now snapd.apparmor
snap warnings
firefox
sudo snap remove firefox
sudo snap install firefox
firefox
which firefox
ls snap/firefox/
ls snap/firefox/current
firefox 
```

I then had to manually install the application shortcut and icon for Firefox.

## ROS installation

Followed the instructions for ROS Lyrical Luth. These were the commands used:

```bash
locale
sudo apt install software-properties-common
sudo add-apt-repository universe
sudo apt update && sudo apt install curl -y
export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F'"' '{print $4}')
curl -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo ${UBUNTU_CODENAME:-${VERSION_CODENAME}})_all.deb"
sudo dpkg -i /tmp/ros2-apt-source.deb
sudo apt update && sudo apt install ros-dev-tools
sudo apt install ros-lyrical-desktop
```

Added these lines to the bottom of my `~/.bash_aliases` file

```bash
# ROS
source /opt/ros/lyrical/setup.bash
source ~/ws/install/setup.bash
```

As this PC is only ever going to be used with one workspace, this makes things easier when auto-starting ROS on power up.

## Workspace Setup 

```bash
mkdir ~/ws
cd ~/ws
mkdir src
cd src
```

Setup new SSH key.

```bash
ssh-keygen -t ed25519 -C "a.j.blight@leeds.ac.uk"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

Added this to my personal account on GitHub.

### Building the Kobuki and Astra camera code

I copied the `src` tree from my main laptop where the code already built and extracted it to the `~/ws/src` directory.  Then I tried to build it.  The following extra packages needed to be installed.

```bash
"sudo apt install -y libuvc-dev \
    libgoogle-glog-dev \
    ros-lyrical-camera-info-manager \
    ros-lyrical-image-publisher"
```

This build completed.

### Building the NAV2 code

I wanted to use the `Nav2` stack for SLAM, so installed a bunch of packages:

```bash 
sudo apt install -y \
ros-lyrical-nav2-amcl \
ros-lyrical-nav2-behavior-tree \
ros-lyrical-nav2-behaviors \
ros-lyrical-nav2-bt-navigator \
ros-lyrical-nav2-controller \
ros-lyrical-nav2-core \
ros-lyrical-nav2-costmap-2d \
ros-lyrical-nav2-lifecycle-manager \
ros-lyrical-nav2-map-server \
ros-lyrical-nav2-msgs \
ros-lyrical-nav2-planner \
ros-lyrical-nav2-ros-common \
ros-lyrical-nav2-route \
ros-lyrical-nav2-rviz-plugins \
ros-lyrical-nav2-util \
ros-lyrical-nav2-velocity-smoother \
ros-lyrical-nav2-voxel-grid 
```

This was because ROS Lyrical is missing the Nav2 meta package that installs the fullstack and more importantly it is also missing the `nav2_bringup` package.  This meant that I then had to clone the [`nav2` repo](https://github.com/ros-navigation/navigation2) and build the entire stack.  This has taken several hours. 

Also had to install this package:

```bash
sudo apt install ros-lyrical-ament-cmake-google-benchmark
```

## Performance issues

The laptop struggles a lot when building the code. `colcon build` does the build OK but prevents anything else working.  VSCode also seems to slow the PC down, even though it shouldn't.

I changed from using `colcon build` to using `colcon build --parallel-executors 1 --executor sequential` but that still used all of the CPUs (4 x `ccplus1` threads running).  I suspect that `--parallel-executors 1` and `--executor sequential` equate to the same thing!  The `--parallel-executors` limits the number of packages that are being built at the same time, but has no effect on the number of CPUs that `make` uses.

Changed to this:

```bash 
MAKEFLAGS="-j2 -l2" colcon build --executor sequential
```

and I was able to edit while building.


