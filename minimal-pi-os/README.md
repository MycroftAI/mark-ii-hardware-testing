# Minimal Mark II with Raspberry Pi OS

Setup script and pre-compiled binaries for using Mark II microphone and speaker in Raspberry Pi OS Lite 64-bit (bullseye).

Contains pre-built kernel module from [XMOS source](https://github.com/xmos/vocalfusion-rpi-setup).

1. Install Raspbery Pi OS Lite 64-bit based on bullseye [1]
    * After burning image:
        * Copy userconf.txt to /boot (user=pi, password=raspberry)
        * Add an empty file named ssh to /boot (enable SSH)
    * `uname -a` should yield `Linux raspberrypi 5.15.32-v8+ #1538 SMP PREEMPT Thu Mar 31 19:40:39 BST 2022 aarch64 GNU/Linux`
2. Enable hardware
    * On device, run `sudo raspi-config` and enable I2C & SPI in Interface Options
    * Reboot
3. Install packages
    * `sudo apt-get update`
    * `sudo apt-get install --yes python3 python3-venv python3-pip`
4. Copy binaries/libraries
    * Copy contents of `usr` directory to `/usr`
5. Copy script and files
    * Copy contents of `home/pi` to `/home/pi`
6. Run script
    * Run `./start-xmos.sh` after each boot
    * Maybe add `@reboot /home/pi/start-xmos.sh` to crontab? 

[1] https://downloads.raspberrypi.org/raspios_lite_armhf/images/raspios_lite_armhf-2022-04-07/2022-04-04-raspios-bullseye-armhf-lite.img.xz
