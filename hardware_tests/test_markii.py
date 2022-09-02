import sys
import asyncio
sys.path.append("/home/pi/") 
import os
import signal
from time import sleep, time
from subprocess import Popen, PIPE
from detect_markii import EnclosureCapabilities
from utils.csv_file import write_test_results_to_file
from utils.utils import CommandExecutor, fix_cmd, LogicalVolume, GREEN, RED, NC
from utils.async_touch import TouchEvent
from utils.async_button import AsyncButtons
"""
   MarkII Production Hardware Test Program

  Goal:  total time < 45 seconds pass or 1 minute worst case fail

  General logic:
    1) IF NOT M2, BAIL
    2) IF NOT SJ201, BAIL
    3) INIT AMP
    4) AUDIO TEST
    5) BUTTON TEST
    6) LEDS TEST
    7) MIC TEST
    8) WRITE TEST REPORT ENTRY
"""
sj201_board_types = {
    0:"None",
    1:"Old",
    2:"New",
    }
board_type = 0   # will be set later

BLACK_LED = (0,0,0)
RED_LED = (255,0,0)
GREEN_LED = (0,255,0)
BLUE_LED = (0,0,255)

activate_button = '24'
right_button = '22'
middle_button = '23'


def volume_good(m2but, lv):
    test_passed = False
    process = Popen(["speaker-test", "-c2", "-twav", "-f2000", "&"])

    to_ctr = 0
    timeout_in_seconds = 30  # very approximate!
    while to_ctr < timeout_in_seconds:
        res = m2but.wait_buttons( [activate_button, right_button, middle_button], 2 )

        if res == activate_button:
            # activate pressed
            break
        elif res == right_button:
            # vol up pressed
            lv.vol_up()
        elif res == middle_button:
            # vol down pressed
            lv.vol_down()
        else:
            # we timed out
            to_ctr += 1

        sleep(0.05)
        to_ctr += 1

    # stop sound
    process.kill()

    # record what happened
    if to_ctr < timeout_in_seconds:
        fix_cmd(board_type, "aplay wavs/did_volume_change.wav")
        fix_cmd(board_type, "aplay wavs/confirm_yesno.wav &")

        res = m2but.wait_buttons( [right_button,middle_button], 10 )
        if res == right_button:
            test_passed = True

    else:
        #print("Error - volume test timed out!")
        pass

    return test_passed


def fan_good(m2but, fc, led_color, leds):
    test_passed = False
    fan_speed = 50
    led_color = (0,0,255)

    for x in range(6):
        leds._set_led(x,(0,0,255))
    leds.show()

    to_ctr = 0
    timeout_in_seconds = 30  # very approximate!
    while to_ctr < timeout_in_seconds:
        res = m2but.wait_buttons( [activate_button, right_button, middle_button], 2 )

        if res == activate_button:
            # activate pressed
            break
        elif res == right_button:
            # vol up pressed
            if fan_speed < 100:
                fan_speed += 10
                fc.set_fan_speed(fan_speed)
                which_led = int( fan_speed / 10 )
                leds._set_led(which_led, led_color)
                leds.show()
        elif res == middle_button:
            # vol down pressed
            if fan_speed > 0:
                which_led = int( fan_speed / 10 )
                leds._set_led(which_led, (0,0,0)) 
                leds.show()
                fan_speed -= 10
                fc.set_fan_speed(fan_speed)
        else:
            # we timed out
            to_ctr += 1

        sleep(0.05)
        to_ctr += 1

    # record what happened
    if to_ctr < timeout_in_seconds:
        fix_cmd(board_type, "aplay wavs/did_fan_change.wav")
        fix_cmd(board_type, "aplay wavs/confirm_yesno.wav &")

        res = m2but.wait_buttons( [right_button,middle_button], 10 )
        if res == right_button:
            test_passed = True

    else:
        #print("Error - fan test timed out!")
        pass

    return test_passed



## like 'if main', but no indent required :-)
start_time = time()
print("\n\n\n\n\n\n\n\n\n\n\n")
print("************************************")
print("** Starting MarkII Hardware Tests **")
print("************************************")
print("\n")

hc = EnclosureCapabilities()     # environment/cpu
serial_number = hc.get_serial_number().strip()
print("Serial Number:%s" % (serial_number,))

fail_tag = "%sFail%s" % (RED,NC)
pass_tag = "%sPass%s" % (GREEN,NC)

cpu = fail_tag
touch_screen = fail_tag
touch_screen_working = fail_tag
memory = fail_tag
storage = fail_tag
recording_test = fail_tag
volume_test = fail_tag
button_right_test = fail_tag
button_left_test = fail_tag
slider_test = fail_tag
brightness_test = fail_tag
camera_test = fail_tag
blue_test = fail_tag
fan_test = fail_tag

# whats the environment look like?
if hc.mice[0]['name'] == 'raspberrypi-ts' and hc.screens[0]['name'] == 'vc4drmfb':
    res = hc.screens[0]['resolution']
    res = res.replace(",", " by ")
    print("Touch screen found - resolution is %s" % (res,))
    #os.system("aplay wavs/touch_screen_found.wav")
    touch_screen = pass_tag
else:
    print("Error - touch screen NOT found!")
    #os.system("aplay wavs/no_touch_screen.wav")

mem_size = int( hc.get_memory_size() )
#if mem_size != '1892728':
if mem_size < 1000000 or  mem_size > 4000000:
    print("Error - unexpected memory size = %s" % (mem_size,))
    #os.system("aplay wavs/memory_bad.wav")
else:
    print("Memory size = %s kb" % (mem_size,))
    #os.system("aplay wavs/memory_good.wav")
    memory = pass_tag

if hc.cpu_is_pi4():
    print("CPU == MarkII")
    cpu = pass_tag
else:
    print("CPU <> MarkII")

disk_total, disk_available = hc.get_storage_info()
if disk_total != "14G":
    print("Warning, storage does not look like a MarkII.")
    #os.system("aplay wavs/storage_bad.wav")
else:
    print("Storage looks like this is a MarkII.")
    print("Total Disk Storage: %s, Available Disk Storage: %s" % (disk_total,disk_available))
    #os.system("aplay wavs/storage_good.wav")
    storage = pass_tag

if touch_screen != pass_tag or memory != pass_tag or storage != pass_tag or cpu != pass_tag:
    print("%sNot a MarkII - Aborting Tests!%s" % (RED,NC))
    exit(-1)

# we believe this to be a pi4 or close enough

cmd = "python hardware_tests/auto_detect_sj201.py"
process = Popen(cmd, stdout=PIPE, stderr=None, shell=True)
output = process.communicate()[0]

board_type = process.wait()

print("SJ201 board_type is %s ---> %s" % (board_type, sj201_board_types[board_type]))
print("*** MarkII Environment Tests %sPassed%s **" % (GREEN,NC))

if board_type == 0:
    print("%sNo SJ201 Detected%s - Aborting Tests!" % (RED,NC))
    exit(-2)

##################################
# we believe we found an sj201   #
# and we believe we are on a pi4 #
##################################
m2but = AsyncButtons()
print("*** %sFound%s %s Style SJ201 ***" % (GREEN,NC,sj201_board_types[board_type]))
if board_type == 1:
    from ledtest_old import Led
    from old_fan import FanControl
else:
    from ledtest_new import Led
    from new_fan import FanControl

leds = Led()

# turn off LEDs
for x in range(12):
    leds._set_led(x,BLACK_LED)
leds.show()

lv = LogicalVolume(leds, board_type, BLUE_LED)
fc = FanControl()

#################
## Start Tests ##
#################
fix_cmd(board_type, "aplay wavs/activate_begin.wav &")

print("You have one minute to press the big round Activate button")
print("If this times out I will assume the button is broken and fail this device")

buttons = [activate_button,]
res = m2but.wait_buttons(buttons, 60)
if res == -1:
    # activate button failed!
    print("Activate button timeout, %sDevice Failed!%s" % (RED,NC)) 
    print("Press Activate button three times fast to rerun tests") 
    print("or power off device to fail it")
    # TODO
    # write the failure row to the csv file
    # assume they will power off in which case the device will show as failed 
    # BUT ...
    # if activate pressed 3 times we will remove the csv row and restart the system
else:
    # we know the activate button is working
    ################
    # button tests #
    ################
    print("\nButton Tests\n-----------")
    print("Push the Right button.")
    print("This test will time out after 5 seconds.")
    fix_cmd(board_type, "aplay wavs/button_right.wav &")
    buttons = [right_button,]
    res = m2but.wait_buttons(buttons, 10)
    if res != -1:
        button_right_test = pass_tag

    print("Push the Middle button.")
    print("This test will time out after 5 seconds.")
    fix_cmd(board_type, "aplay wavs/button_middle.wav &")
    buttons = [middle_button,]
    res = m2but.wait_buttons(buttons, 10)
    if res != -1:
        button_left_test = pass_tag

    # TODO do we have two working buttons?

    ###############
    # slider test #
    ###############
    # note - we should leave the mic in the unmuted 
    # state to reduce strain on our customer svc dept.
    SLIDER_DELAY = 0.5
    SLIDER_TIMEOUT = 20
    # note - 0 is to the left and 1 is to the right
    # we assume 1 is muted and 0 is not muted
    mic_is_muted = False
    if '1' == m2but.get_mic_switch():
        mic_is_muted = True

    mic_test_passed = False
    if not mic_is_muted:
        fix_cmd(board_type, "aplay wavs/slide_right.wav &")
        print("Slide far left button to the right")
        to_ctr = 0
        while to_ctr < SLIDER_TIMEOUT and m2but.get_mic_switch() == '0':
            sleep(SLIDER_DELAY)
            to_ctr += 1

        if to_ctr != SLIDER_TIMEOUT:
            fix_cmd(board_type, "aplay wavs/slide_left.wav &")
            print("Slide far left button to the left")
            to_ctr = 0
            while to_ctr < SLIDER_TIMEOUT and m2but.get_mic_switch() == '1':
                sleep(SLIDER_DELAY)
                to_ctr += 1
            if to_ctr != SLIDER_TIMEOUT:
                mic_test_passed = True
    else:
        fix_cmd(board_type, "aplay wavs/slide_left.wav &")
        print("Slide far left button to the left")
        to_ctr = 0
        while to_ctr < SLIDER_TIMEOUT and m2but.get_mic_switch() == '1':
            sleep(SLIDER_DELAY)
            to_ctr += 1
        if to_ctr != SLIDER_TIMEOUT:
            fix_cmd(board_type, "aplay wavs/slide_right.wav &")
            print("Slide far left button to the right")
            to_ctr = 0
            while to_ctr < SLIDER_TIMEOUT and m2but.get_mic_switch() == '0':
                sleep(SLIDER_DELAY)
                to_ctr += 1
            if to_ctr != SLIDER_TIMEOUT:
                mic_test_passed = True

    if mic_test_passed:
        slider_test = pass_tag

    print("Mic mute/slider test passed = %s" % (slider_test,))

    ###############
    # volume test #
    ###############
    print("\nVolume Tests\n------------")
    print("Use the right and middle buttons to change the volume. Press Activate when done")
    fix_cmd(board_type, "aplay wavs/vol_test1.wav")
    fix_cmd(board_type, "aplay wavs/vol_test2.wav")

    for x in range(6):
        sleep(0.1) # indicates led code neds some attention! don't auto show!
        leds._set_led(x,BLUE_LED)
    leds.show()

    if volume_good(m2but, lv):
        volume_test = pass_tag

    ############
    # test fan #
    ############
    print("Fan Test, use buttons to change fan speed. Press Activate when done.")
    fix_cmd(board_type, "aplay wavs/change_fan_speed.wav")
    fix_cmd(board_type, "aplay wavs/activate_to_end.wav")

    if fan_good(m2but, fc, BLUE_LED, leds):
        fan_test = pass_tag

    #############
    # test LEDs #
    #############
    print("LED Brightness test")
    fix_cmd(board_type, "aplay wavs/starting_led_brightness_tests.wav")
    if board_type == 1:
        os.system("python hardware_tests/ledtest_old.py")
    else:
        os.system("sudo python hardware_tests/ledtest_new.py")

    fix_cmd(board_type, "aplay wavs/leds_get_brighter.wav")
    fix_cmd(board_type, "aplay wavs/confirm_yesno.wav &")

    res = m2but.wait_buttons( [right_button,middle_button], 10 )
    if res == right_button:
        brightness_test = pass_tag

    ############
    # mic test #
    ############
    print("test mic")
    fix_cmd(board_type, "aplay wavs/record.wav")

    cmd = "bash hardware_tests/mic_test_old.sh"
    if board_type == 2:
        cmd = "bash hardware_tests/mic_test_new.sh"

    process = Popen(cmd, stdout=PIPE, stderr=None, shell=True)
    output = process.communicate()[0]
    ret_code = process.wait()
    if ret_code == 0:
        fix_cmd(board_type, "aplay wavs/confirm_yesno.wav &")
        res = m2but.wait_buttons( [right_button,middle_button], 10 )
        if res == right_button:
            recording_test = pass_tag
    else:
        print("Mic test failed energy tests")

    #####################
    # touch screen test #
    #####################
    fix_cmd(board_type, "aplay wavs/touch_the_screen.wav")
    print("Touch the screen")
    loop = asyncio.get_event_loop()
    tse = TouchEvent()
    loop.run_until_complete(tse.main())
    if tse.got_key:
        touch_screen_working = pass_tag

    ###############
    # test camera #
    ###############
    print("Begin Camera Test - Note! make sure the shutter is open!")
    fix_cmd(board_type, "aplay wavs/testing_the_camera.wav")
    fix_cmd(board_type, "aplay wavs/click.wav")
    fix_cmd(board_type, "aplay wavs/click.wav")
    fix_cmd(board_type, "aplay wavs/click.wav")
    fix_cmd(board_type, "ffmpeg -y -framerate 30 -f v4l2 -video_size 800x480 -i /dev/video0 -ss 00:00:03 -frames:v 1 wtf.jpg")
    os.system("sudo fbi -T 1 -d /dev/fb0 wtf.jpg")
    fix_cmd(board_type, "aplay wavs/camera_click.wav")
    fix_cmd(board_type, "aplay wavs/confirm_image.wav")
    fix_cmd(board_type, "aplay wavs/confirm_yesno.wav &")

    res = m2but.wait_buttons( [right_button,middle_button], 10 )
    if res == right_button:
        camera_test = pass_tag

    os.system("sudo killall fbi")
    os.system("rm wtf.jpg")

    ##################
    # test bluetooth #
    ##################
    print("Starting Blue Tooth scan.")
    print("Press the activate button when you see your device.")
    print("Press any other button to cancel the test.")
    os.system("bluetoothctl scan on &")
    fix_cmd(board_type, "aplay wavs/starting_bluetooth_scan.wav")
    fix_cmd(board_type, "aplay wavs/press_activate_when_you_see_device.wav")
    fix_cmd(board_type, "aplay wavs/press_any_to_cancel.wav")
    m2but.wait_buttons([activate_button,right_button,middle_button], 30)
    os.system("killall bluetoothctl")
    if m2but.key_gpio == activate_button:
        blue_test = pass_tag

# write test results here
print("\n          Test Results\n          ------------")
print(" Serial Number [%s]" % (serial_number,))
print("            CPU[%s]" % (cpu,))
print("         Memory[%s]" % (memory,))
print("        Storage[%s]" % (storage,))
print(" Touch Detected[%s]" % (touch_screen,))
print("  Touch Working[%s]" % (touch_screen_working,))
print("         Volume[%s]" % (volume_test,))
print("   Button Right[%s]" % (button_right_test,))
print("    Button Left[%s]" % (button_left_test,))
print("         Slider[%s]" % (slider_test,))
print("     Brightness[%s]" % (brightness_test,))
print("      Recording[%s]" % (recording_test,))
print("         Camera[%s]" % (camera_test,))
print("      Bluetooth[%s]" % (blue_test,))
print("            Fan[%s]" % (fan_test,))

# save results to csv file
csv_data = {
    "serial_number":serial_number,
    "version":board_type,
    "tester":"None",
    "cpu":cpu,
    "memory":memory,
    "storage":storage,
    "touch_screen":touch_screen,
    "volume":volume_test,
    "button_right":button_right_test,
    "button_left":button_left_test,
    "slider":slider_test,
    "brightness":brightness_test,
    "recording":recording_test,
    "touch_working":touch_screen_working,
    "camera":camera_test,
    "bluetooth":blue_test,
    "fan":fan_test,
}

write_test_results_to_file(csv_data)
lv.close()
elapsed = time() - start_time
print("Took %s Seconds" % ( int( elapsed ),) )
print("\n\n\n")

