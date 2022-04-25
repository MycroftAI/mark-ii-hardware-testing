#!/bin/bash

VALID_SYS_INFO="Linux raspberrypi 5.15.32-v8+ #1538 SMP PREEMPT Thu Mar 31 19:40:39 BST 2022 aarch64 GNU/Linux"
ACTUAL_SYS_INFO=$(uname -a)
if [[ "$ACTUAL_SYS_INFO" != "$VALID_SYS_INFO" ]]
then
    echo "Unexpected system information."
    echo "Expected: $VALID_SYS_INFO"
    echo "Got: $ACTUAL_SYS_INFO"
    echo ""
    echo "Ensure you have flashed the 64 bit Raspberry Pi OS Lite."
    exit 1
fi

sudo apt-get update && sudo apt-get upgrade -y

sudo apt-get install --yes python3 python3-venv python3-pip i2c-tools sox

VENV='venv'

if [ ! -d "${VENV}" ]; then
    python3 -m venv --system-site-packages "${VENV}"
    "${VENV}/bin/pip3" install -r requirements.txt
fi

echo "./run-tests.sh" >> $HOME/.bashrc

echo "To finalize image setup:"
echo "1. Launch raspi-config"
echo "2. Select 'Interface Options'"
echo "3. Enable I2C and SPI"
echo "4. Delete os_setup_2.sh"
echo "4. Then shutdown."
