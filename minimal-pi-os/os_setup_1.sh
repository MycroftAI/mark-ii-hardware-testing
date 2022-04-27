#!/bin/bash
BOOT_PARTITION="/media/$USER/boot"
ROOTFS_PARTITION="/media/$USER/rootfs"
PI_USER="pi"

if [[ ! -d $BOOT_PARTITION || ! -d $ROOTFS_PARTITION ]]; then
    echo "ERROR: Cannot detect mounted partitions at:"
    echo "       - $BOOT_PARTITION"
    echo "       - $ROOTFS_PARTITION"
    echo "Please check that the USB is mounted and RPi OS Lite has been flashed."
    exit 1
fi

# Create default user (user=pi, password=raspberry)
cp files/boot/userconf.txt "$BOOT_PARTITION"

# Add required settings
cp files/boot/config.txt "$BOOT_PARTITION"

# Enable SSH access
touch "$BOOT_PARTITION/ssh"

# Copy files to ROOTFS partition
sudo install -o root -g root files/rootfs/usr/bin/* "$ROOTFS_PARTITION/usr/bin/"
sudo cp -r files/rootfs/usr/lib/* "$ROOTFS_PARTITION/usr/lib/"
sudo chown -R root:root "$ROOTFS_PARTITION/usr/lib/aarch64-linux-gnu"

sudo cp -rT "files/rootfs/home/$PI_USER" "$ROOTFS_PARTITION/home/$PI_USER"
