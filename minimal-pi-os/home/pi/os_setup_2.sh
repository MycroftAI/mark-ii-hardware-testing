#!/bin/bash

sudo apt-get update && sudo apt-get upgrade -y

sudo apt-get install --yes python3 python3-venv python3-pip i2c-tools

./start-xmos.sh
