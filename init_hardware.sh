#!/bin/bash
set -ex
VENV='/home/pi/venv'
CURRENT_DIR=$(dirname -- "$(readlink -f "${BASH_SOURCE}")")

if [ ! -d "${VENV}" ]; then
    echo "INSTALLING VENV - this may take some time"
    sleep 3
    sudo apt -y update
    sudo apt -y install i2c-tools
    sudo apt -y install python3-venv
    sudo apt -y install python3-pip
    sudo apt -y install evtest
    sudo apt -y install fbi
    python3 -m venv --system-site-packages "${VENV}"
    source "${VENV}/bin/activate"
    sleep 1
    pip install -r requirements.txt
    sudo pip install rpi_ws281x adafruit-circuitpython-neopixel
    sudo python3 -m pip install --force-reinstall adafruit-blinka
    sudo pip install smbus2
    cp drivers/asoundrc_vf_xvf3510_int .asoundrc

    sudo apt -y install ffmpeg

    deactivate
fi

source "${VENV}/bin/activate"

cd drivers

sh load_i2s_driver.sh || true
sudo ./setup_mclk
sudo ./setup_bclk

raspi-gpio set 16 op
raspi-gpio set 16 dl

raspi-gpio set 27 op
raspi-gpio set 27 dl

sleep 1
raspi-gpio set 16 dh
sleep 1
raspi-gpio set 27 dh
sleep 1

python3 send_image_from_rpi.py --direct app_xvf3510_int_spi_boot_v4_1_0.bin

cd ..

python utils/init_tas5806.py

i2cdetect -a -y 1
aplay wavs/start_listening.wav
