import sys
sys.path.append("/home/pi/") 
import os
import asyncio
from time import sleep, time
from utils.async_touch import TouchEvent

while True:
    os.system("sudo fbi -T 1 -d /dev/fb0 mycroft_logo.jpg")
    # touch screen test #
    os.system("aplay ../wavs/touch_the_screen.wav")
    print("Touch the screen")
    loop = asyncio.get_event_loop()
    tse = TouchEvent()
    loop.run_until_complete(tse.main())
    if tse.got_key:
        print("detected touch")

    os.system("killall aplay")
    os.system("sudo killall fbi")
    os.system("rm wtf.jpg")

    # test camera #
    print("Begin Camera Test - Note! make sure the shutter is open!")
    os.system("aplay ../wavs/click.wav")
    os.system("aplay ../wavs/click.wav")
    os.system("aplay ../wavs/click.wav")
    os.system("ffmpeg -y -framerate 30 -f v4l2 -video_size 800x480 -i /dev/video0 -ss 00:00:03 -frames:v 1 wtf.jpg")
    os.system("sudo fbi -T 1 -d /dev/fb0 wtf.jpg")
    os.system("aplay ../wavs/start_listening.wav")
    os.system("aplay ../wavs/start_listening.wav")
    os.system("aplay ../wavs/start_listening.wav")
    sleep(30)
    os.system("sudo killall fbi")
    os.system("rm wtf.jpg")
