<PRE>
MarkII Hardware Test Image Build Instructions
---------------------------------------------
The MarkII is a Raspberry Pi4 which is a quad core ARM Cortex
SOC with 2GB of RAM and a 16GB USB 3.0 drive. Your basic Pi4
includes 2 USB 3.0 ports, 2 USB 2.0 ports, an Ethernet port,
Bluetooth, WiFi, SD Card interface and 2 HDMI ports.

The MarkII is a Pi4 plus a plug on adapter board known as
the SJ201. The SJ201 provides a TI Amplifier, 3 buttons and
slider, and an XMOS DSP which provides AEC for the dual far
field mic array. Power for the the Pi4 and SJ201 are routed
through the SJ201 which provides power for the amplification
circuits as well as the Raspberry Pi4 proper.

The MarkII also includes a touch screen, variable speed fan,
camera, Texas Instruments TI5806 amplifier and an acoustically
designed audio chamber.

This repository and the instructions below may be used to 
create a bootable image for the MarkII which will run the 
MarkII production tests automatically on boot.

--

Assuming you have a MarkII at IP address 1.2.3.4

1) Burn bullseye lite and configure for ssh so you can ssh in 
to the device. See HERE for instructions.


2) Git clone the hardware test repository 

    git clone bla


3) Copy files to the MarkII

    scp -r mark-ii-hardware-testing/* pi@1.2.3.4:/home/pi/.


3) SSH into the MarkII and run sudo raspi-config
   enable i2c and spi interfaces and legacy camera support
   under performance set the GPU memory to 256.
   select finish and reboot


4) SSH back into the MarkII, edit /boot/config.txt

  4.a) uncomment the line
       #dtparam=i2s=on
  4.b) comment out this line
       dtparam=audio=on

In other words turn on i2s and turn off the default audio device
See Note(2) below.


5) Edit file .bashrc and add these lines to the end of the file

bash /home/pi/init_hardware.sh
bash /home/pi/run_tests.sh

This file is located at /home/pi/.bashrc


6) Reboot - the MarkII should boot into test mode
(power off or sudo shutdown -r now)


7) To test the audio path run 'arecord junk.wav' then 'aplay junk.wav' 


Notes:
    1) the first time you reboot it will take about 15 minutes.
       This is because if it does not find the python environment (located at
       /home/pi/venv/) it will create it and this can take some time. Subsequent
       reboots will detect the presence of the venv/ dir and boot much faster.

    2) you will need to use sudo so 
   
       sudo raspi-config

          and

      sudo vi /boot/config.txt
          or
      sudo nano /boot/config.txt

    3) a file named test_results.csv will be updated after each test run.
    
    4) You need to have the MarkII connected to the internet when you build
       the image, but internet connectivity is not required to actually run
       the image.

    5) you will need to run ./init_hardware.sh on each reboot. ./run_tests.sh
       will run the production hardware tests, but these were set to both run
       automatically on reboot so you don't need to worry about this.



MANIFEST
--------
wavs/
    a directory of wav files

drivers/
    a directory full of driver type code for 
    the SJ201 - see below for further detail

hardware_tests/
    a directory full of assembly line hardware 
    tests for the MarkII - also see below

utils/
    a directory of utility functions
    also see below

README
    this file

run_tests.sh
    runs the hardware tests

requirements.txt
    initial venv install python requirements

init_hardware.sh
    initializes the sj201 and installs the venv 
    if missing. note rm -Rf venv will force
    an update on the next run


The drivers/ directory
----------------------
app_xvf3510_int_spi_boot_v4_1_0.bin
    the xmos dsp configuration bundle

asoundrc_vf_xvf3510_int
    default asoundrc for sj201

i2s_master_loader.ko
    loads the .ko file into the kernel

init_tas5806.py
    ti amplifier initialization code

load_i2s_driver.sh
    loads the sj201 i2s driver

send_image_from_rpi.py
    sends the xmos dsp configuration bundle to the sj201

setup_bclk
    provides basic i2s bit clock

setup_mclk
    provides basic i2s master clock


The hardware_tests/ directory
-----------------------------
auto_detect_sj201.py
detect_markii.py
__init__.py
ledtest_new.py
ledtest_old.py
mic_test_new.sh
mic_test_old.sh
MycroftLed.py
test_markii.py


The utils/ directory
--------------------
async_button.py
async_touch.py
csv_file.py
__init__.py
init_tas5806.py
set_volume_tas5806.py
utils.py

</PRE>
