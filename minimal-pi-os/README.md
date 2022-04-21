# Minimal Mark II with Raspberry Pi OS

Setup script and pre-compiled binaries for using Mark II microphone and speaker in Raspberry Pi OS Lite 64-bit (bullseye).

Contains pre-built kernel module from [XMOS source](https://github.com/xmos/vocalfusion-rpi-setup).

1. Install Raspbery Pi OS Lite 64-bit based on bullseye [1]
    * After burning image run `./os_setup_1.sh` to:
        * Copy userconf.txt to /boot (user=pi, password=raspberry)
        * Add an empty file named ssh to /boot (enable SSH)
        * Copy contents of `usr` directory to `/usr`
        * Copy contents of `home/pi` to `/home/pi`
    * After booting the OS `uname -a` should yield `Linux raspberrypi 5.15.32-v8+ #1538 SMP PREEMPT Thu Mar 31 19:40:39 BST 2022 aarch64 GNU/Linux`
2. Enable hardware
    * On device, run `sudo raspi-config` and enable I2C & SPI in Interface Options
    * Reboot
3. After rebooting, on device run `./os_setup_2.sh` to:
    * Install system packages
        * `sudo apt-get update`
        * `sudo apt-get install --yes python3 python3-venv python3-pip`
    * Install python requirements
        * `pip3 install -r requirements.txt`
    * Run `./start-xmos.sh` after each boot

[1] https://downloads.raspberrypi.org/raspios_lite_arm64/images/raspios_lite_arm64-2022-04-07/2022-04-04-raspios-bullseye-arm64-lite.img.xz
