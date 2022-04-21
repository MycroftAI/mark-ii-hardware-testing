#!/bin/bash

sudo apt-get update && sudo apt-get upgrade -y

sudo apt-get install --yes python3 python3-venv python3-pip i2c-tools

{
    echo ""
    echo "# Load I2S driver and start the XMOS chip"
    echo "./start-xmos.sh"
    echo ""
} >> $HOME/.bashrc

./start-xmos.sh
