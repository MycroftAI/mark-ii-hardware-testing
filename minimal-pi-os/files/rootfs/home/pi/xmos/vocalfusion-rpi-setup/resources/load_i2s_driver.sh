sleep 1
sudo insmod /home/pi/xmos/vocalfusion-rpi-setup/loader/i2s_master/i2s_master_loader.ko
# Run Alsa at startup so that alsamixer configures
arecord -d 1 > /dev/null 2>&1
aplay dummy > /dev/null 2>&1