#!/bin/bash
set -ex

VENV='/home/pi/venv'

CURRENT_DIR=$(dirname -- "$(readlink -f "${BASH_SOURCE}")")

if [ ! -d "${VENV}" ]; then
    python3 -m venv --system-site-packages "${VENV}"
    "${VENV}/bin/pip3" install -r requirements.txt
fi

source "${VENV}/bin/activate"

sh ${CURRENT_DIR}/vocalfusion-rpi-setup/resources/load_i2s_driver.sh || true

sudo setup_mclk
sudo setup_bclk

sleep 1
gpio -g mode 16 out 
gpio -g mode 27 out 
gpio -g write 16 1 
gpio -g write 27 1 
sleep 1

python3 ${CURRENT_DIR}/send_image_from_rpi.py --direct ${CURRENT_DIR}/app_xvf3510_int_spi_boot_v4_1_0.bin

sleep 1
