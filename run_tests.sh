#!/bin/bash

# make sure you have run init_hardware.sh
# before running this !

source /home/pi/venv/bin/activate

## auto detect sj201 if present
python hardware_tests/auto_detect_sj201.py

RES=$?
echo "SJ201 Board Type=$RES"

if [ $RES == 0 ]
then
   echo 'No SJ201, no tests for you!'
elif [ $RES == 1 ]
then
   echo 'Old SJ201 Discovered'
   python utils/init_tas5806.py
   python hardware_tests/test_markii.py
else
   echo 'New SJ201 Discovered'
   python utils/init_tas5806.py
   sudo python hardware_tests/test_markii.py
fi

