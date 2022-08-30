from subprocess import Popen, PIPE
import os
"""
try to auto detect sj201 board type
if none bail. if found determine version
(old or new) and run appropriate tests
returns 0 for None, 1 for old sj201 2 for new sj201
"""
tiny_address = "04"
xmos_address = "2c"
ti_address = "2f"

def verify_xmos():
    result = False
    cmd = "drivers/vfctrl_i2c GET_I2S_RATE"
    process = Popen(cmd, stdout=PIPE, stderr=None, shell=True)
    output = process.communicate()[0] 
    if output:
        output = output.decode('utf-8')
        if output.find("48000") > -1:
            result = True
    return result

## TODO 
def verify_tiny():
    result = True
    return result

def verify_ti():
    result = True
    return result

def test_sj201_new():
    #print("Running New SJ201 Tests")
    return True

def test_sj201_old():
    #print("Running Old SJ201 Tests")
    return True


#################
## pseudo main ##
#################
tests_passed = False
cmd = "i2cdetect -a -y 1 | grep %s" % (tiny_address,)
process = Popen(cmd, stdout=PIPE, stderr=None, shell=True)
tiny_is_present = True if process.communicate()[0] else False

cmd = "i2cdetect -a -y 1 | grep %s" % (xmos_address,)
process = Popen(cmd, stdout=PIPE, stderr=None, shell=True)
xmos_is_present = True if process.communicate()[0] else False

cmd = "i2cdetect -a -y 1 | grep %s" % (ti_address,)
process = Popen(cmd, stdout=PIPE, stderr=None, shell=True)
ti_is_present = True if process.communicate()[0] else False

# just because something exists does not mean it is one of us

if tiny_is_present:
    tiny_is_present = verify_tiny()

if xmos_is_present:
    xmos_is_present = verify_xmos()

if ti_is_present:
    ti_is_present = verify_ti()

sj201_type = 'none'
if ti_is_present and xmos_is_present:
    sj201_type = 'new'
    if tiny_is_present and xmos_is_present and ti_is_present:
        # older boards have all 3, newer boards have no at tiny
        sj201_type = 'old'

if sj201_type == 'none':
    # if no sj201 detected, bail
    #os.system("aplay wavs/warning_no_sj201.wav")
    exit(0)

# we believe we have an sj201
#os.system("aplay wavs/found_sj201.wav")
if sj201_type == 'new':
    sj201_type = 2
    #os.system("aplay wavs/newest_sj201.wav")
    tests_passed = test_sj201_new()
else:
    sj201_type = 1
    #os.system("aplay wavs/older_sj201.wav")
    tests_passed = test_sj201_old()

exit(sj201_type)

