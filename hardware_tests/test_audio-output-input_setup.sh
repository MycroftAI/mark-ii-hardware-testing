#!/bin/sh
# 
# Install system requirements for audio output-input tests

sudo apt-get -y remove libportaudio2
sudo apt-get -y install libasound2-dev

# TODO - why are we installing different versions on top of each other?
git clone -b alsapatch https://github.com/gglockner/portaudio

cp ../files/home/mycroft/PCBtests/pa_linux_alsa.c /home/mycroft/portaudio/src/hostapi/alsa/pa_linux_alsa.c
pushd portaudio
./configure && make
sudo make install
sudo ldconfig
popd

wget http://files.portaudio.com/archives/pa_stable_v190600_20161030.tgz
tar xvzf pa_stable_v190600_20161030.tgz
pushd portaudio/
cp ../files/home/mycroft/PCBtests/pa_linux_alsa.c  /home/mycroft/portaudio/src/hostapi/alsa/pa_linux_alsa.c
./configure && make
sudo make install
ldconfig
popd

sudo pip3 install precise-runner