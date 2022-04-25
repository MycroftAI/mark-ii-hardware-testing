#!/bin/sh
# 
# Install system requirements for all hardware test 

# Universal system prep and common dependencies
sudo apt-get update --fix-missing
sudo apt-get install git python3-pip

# test_buttons.py
sudo apt-get install -y python3-gpiozero python-gpiozero

# test_tas5806_amp.py
sudo pip3 install smbus2

# test_audio-input-output.py
./test_audio-output-input_setup.sh