#!/usr/bin/env bash

install_libs(){
    #sudo apt install -y ocl-icd
    #sudo apt install -y ocl-icd-devel
    apt update
    apt install -y opencl-headers
    echo "Installing Vitis ${TOOLVERSION} libraries"
    /proj/octfpga-PG0/tools/Xilinx/Vitis/${TOOLVERSION}/scripts/installLibs.sh
    bash -c "echo 'source /proj/octfpga-PG0/tools/Xilinx/Vitis/${TOOLVERSION}/settings64.sh' >> /etc/profile"
}

install_dev_platform(){
    echo "Install dev platform"
    cp /proj/octfpga-PG0/tools/dev_platform/${TOOLVERSION}/*.deb /tmp
    apt install /tmp/xilinx-u280*.deb
}

install_xrt() {
    echo "Install XRT"
    if [[ "$OSVERSION" == "ubuntu-20.04" ]] || [[ "$OSVERSION" == "ubuntu-22.04" ]]; then
        echo "Ubuntu XRT install"
        echo "Installing XRT dependencies..."
        apt update
        echo "Installing XRT package..."
        apt install -y $XRT_BASE_PATH/$TOOLVERSION/$OSVERSION/$XRT_PACKAGE
    fi
    sudo bash -c "echo 'source /opt/xilinx/xrt/setup.sh' >> /etc/profile"
    sudo bash -c "echo 'source $VITIS_BASE_PATH/$TOOLVERSION/settings64.sh' >> /etc/profile"
}

check_shellpkg() {
    if [[ "$OSVERSION" == "ubuntu-20.04" ]] || [[ "$OSVERSION" == "ubuntu-22.04" ]]; then
        PACKAGE_INSTALL_INFO=`apt list --installed 2>/dev/null | grep "$PACKAGE_NAME" | grep "$PACKAGE_VERSION"`
    else
        echo "Unsupported OS: $OSVERSION"
        exit 1 
    fi
}

check_xrt() {
    if [[ "$OSVERSION" == "ubuntu-20.04" ]] || [[ "$OSVERSION" == "ubuntu-22.04" ]]; then
        XRT_INSTALL_INFO=`apt list --installed 2>/dev/null | grep "xrt" | grep "$XRT_VERSION"`
    else
        echo "Unsupported OS: $OSVERSION"
        exit 1 
    fi
}

install_xbflash() {
    cp -r $XBFLASH_BASE_PATH/${OSVERSION} /tmp
    echo "Installing xbflash."
    if [[ "$OSVERSION" == "ubuntu-20.04" ]] || [[ "$OSVERSION" == "ubuntu-22.04" ]]; then
        apt install /tmp/${OSVERSION}/*.deb
    else
        echo "Unsupported OS: $OSVERSION"
        exit 1 
    fi 
}

check_requested_shell() {
    SHELL_INSTALL_INFO=`/opt/xilinx/xrt/bin/xbmgmt examine | grep "$DSA"`
}

check_factory_shell() {
    SHELL_INSTALL_INFO=`/opt/xilinx/xrt/bin/xbmgmt examine | grep "$FACTORY_SHELL"`
}

install_u280_shell() {
    check_shellpkg
    if [[ $? != 0 ]]; then
        # echo "Download Shell package"
        # wget -cO - "https://www.xilinx.com/bin/public/openDownload?filename=$SHELL_PACKAGE" > /tmp/$SHELL_PACKAGE
        if [[ $SHELL_PACKAGE == *.tar.gz ]]; then
            echo "Untar the package. "
            tar xzvf $SHELL_BASE_PATH/$TOOLVERSION/$OSVERSION/$SHELL_PACKAGE -C /tmp/
            rm /tmp/$SHELL_PACKAGE
        fi
        echo "Install Shell"
        if [[ "$OSVERSION" == "ubuntu-20.04" ]] || [[ "$OSVERSION" == "ubuntu-22.04" ]]; then
            echo "Install Ubuntu shell package"
            apt-get install -y /tmp/xilinx*
        elif [[ "$OSVERSION" == "centos-8" ]]; then
            echo "Install CentOS shell package"
            yum install -y /tmp/xilinx*
        fi
        rm /tmp/xilinx*
    else
        echo "The package is already installed. "
    fi
}

install_libs() {
    echo "Installing libs."
    sudo $VITIS_BASE_PATH/$TOOLVERSION/scripts/installLibs.sh
}

XRT_BASE_PATH="/proj/octfpga-PG0/tools/deployment/xrt"
SHELL_BASE_PATH="/proj/octfpga-PG0/tools/deployment/shell"
XBFLASH_BASE_PATH="/proj/octfpga-PG0/tools/xbflash"
VITIS_BASE_PATH="/proj/octfpga-PG0/tools/Xilinx/Vitis"
CONFIG_FPGA_PATH="/proj/octfpga-PG0/tools/post-boot/u280/ubuntu-$(lsb_release -rs)"

OSVERSION=`grep '^ID=' /etc/os-release | awk -F= '{print $2}'`
OSVERSION=`echo $OSVERSION | tr -d '"'`
VERSION_ID=`grep '^VERSION_ID=' /etc/os-release | awk -F= '{print $2}'`
VERSION_ID=`echo $VERSION_ID | tr -d '"'`
OSVERSION="$OSVERSION-$VERSION_ID"
REMOTEDESKTOP=$1
TOOLVERSION=$2
SCRIPT_PATH=/local/repository
COMB="${TOOLVERSION}_${OSVERSION}"
XRT_PACKAGE=`grep ^$COMB: $SCRIPT_PATH/spec.txt | awk -F':' '{print $2}' | awk -F';' '{print $1}' | awk -F= '{print $2}'`
SHELL_PACKAGE=`grep ^$COMB: $SCRIPT_PATH/spec.txt | awk -F':' '{print $2}' | awk -F';' '{print $2}' | awk -F= '{print $2}'`
DSA=`grep ^$COMB: $SCRIPT_PATH/spec.txt | awk -F':' '{print $2}' | awk -F';' '{print $3}' | awk -F= '{print $2}'`
PACKAGE_NAME=`grep ^$COMB: $SCRIPT_PATH/spec.txt | awk -F':' '{print $2}' | awk -F';' '{print $5}' | awk -F= '{print $2}'`
PACKAGE_VERSION=`grep ^$COMB: $SCRIPT_PATH/spec.txt | awk -F':' '{print $2}' | awk -F';' '{print $6}' | awk -F= '{print $2}'`
XRT_VERSION=`grep ^$COMB: $SCRIPT_PATH/spec.txt | awk -F':' '{print $2}' | awk -F';' '{print $7}' | awk -F= '{print $2}'`
FACTORY_SHELL="xilinx_u280_GOLDEN_8"
NODE_ID=$(hostname | cut -d'.' -f1)

check_xrt
if [ $? == 0 ]; then
    echo "XRT is already installed."
else
    echo "XRT is not installed. Attempting to install XRT..."
    install_xrt

    check_xrt
    if [ $? == 0 ]; then
        echo "XRT was successfully installed."
    else
        echo "Error: XRT installation failed."
        exit 1
    fi
fi

install_libs
check_shellpkg
if [ $? == 0 ]; then
    echo "Shell is already installed."
else
    echo "Shell is not installed. Installing shell..."
    install_u280_shell
    check_shellpkg
    if [ $? == 0 ]; then
        echo "Shell was successfully installed."
    else
        echo "Error: Shell installation failed."
        exit 1
    fi
fi

install_dev_platform

if [ $REMOTEDESKTOP == "True" ] ; then
    echo "Installing remote desktop software"
    apt install -y ubuntu-gnome-desktop
    echo "Installed gnome desktop"
    systemctl set-default multi-user.target
    apt install -y tigervnc-standalone-server
    echo "Installed vnc server"
fi

echo "Done running startup script."
exit 0
