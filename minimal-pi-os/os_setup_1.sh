#!/bin/bash
BOOT_PARTITION="/media/$USER/boot"
ROOTFS_PARTITION="/media/$USER/rootfs"
PI_USER="pi"

if [ ! -d $BOOT_PARTITION ]; then
    echo "ERROR: Cannot detect mounted boot partition at $BOOT_PARTITION"
    echo "Please check that the USB is mounted and RPi OS Lite has been flashed."
    exit 1
fi

# Create default user (user=pi, password=raspberry)
cp userconf.txt $BOOT_PARTITION

# Enable SSH access
touch $BOOT_PARTITION/ssh

# Copy files to ROOTFS partition
sudo install -o root -g root usr/bin/* $ROOTFS_PARTITION/usr/bin/
sudo cp -r usr/lib/* $ROOTFS_PARTITION/usr/lib/
sudo chown -R root:root $ROOTFS_PARTITION/usr/lib/aarch64-linux-gnu

sudo cp -r home/$PI_USER/* $ROOTFS_PARTITION/home/$PI_USER/
# sudo chown -R $PI_USER:$PI_USER $ROOTFS_PARTITION/home/$PI_USER/*
