#!/bin/bash
set -ex

# Load I2S driver and start the XMOS chip
./xmos/start-xmos.sh

# Execute tests
source venv/bin/activate
echo "** NOTE: FS Error messages below are expected."
python3 tests/test_tas5806.py
echo "** NOTE: FS Error messages above are expected."

./tests/test_mic.sh

python3 tests/test_buttons.py

# python3 tests/test_leds.py
