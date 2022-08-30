import subprocess
import os


class EnclosureCapabilities:
    name_line = 'N: Name="'
    keyboard_line = "H: Handlers=sysrq kbd"
    mouse_line = "H: Handlers=mouse"

    def __init__(self):
        self.pi_serial_number = '0'
        self.mice = []
        self.keyboards = []
        self.screens = []

        self.caps = self._get_capabilities()

        self.mice = self.caps["mice"]
        self.keyboards = self.caps["keyboards"]
        self.screens = self.caps["screens"]


    def execute_cmd(self, cmd):
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        out, err = process.communicate()

        try:
            out = out.decode("utf8")
        except Exception:
            pass

        try:
            err = err.decode("utf8")
        except Exception:
            pass

        return out, err


    def _get_capabilities(self):
        # query input devices

        cmd = ["cat", "/proc/bus/input/devices"]
        out, err = self.execute_cmd(cmd)

        if err:
            # print("Error trying to read input devices:%s" % (err,))
            pass
        else:
            for line in out.split("\n"):
                if line != "":
                    if line.startswith(self.name_line):
                        dev_name = line[len(self.name_line):]
                        dev_name = dev_name[:-1]
                    elif line.startswith(self.keyboard_line):
                        kbd_obj = {"name": dev_name, "extra": ""}
                        self.keyboards.append(kbd_obj)
                    elif line.startswith(self.mouse_line):
                        extra = ""
                        if dev_name.startswith("FT5406 memory based driver"):
                            extra = "Touch Screen"
                        mouse_obj = {"name": dev_name, "extra": extra}
                        self.mice.append(mouse_obj)

        # query output devices.

        screen_name = ""
        cmd = ["cat", "/sys/class/graphics/fb0/name"]
        out, err = self.execute_cmd(cmd)

        if err:
            # print("Error trying to read output devices:%s" % (err,))
            pass
        else:
            screen_name = out.strip()

        screen_resolution = ""
        cmd = ["cat", "/sys/class/graphics/fb0/virtual_size"]
        out, err = self.execute_cmd(cmd)

        if err:
            # print("Error trying to read output devices:%s" % (err,))
            pass
        else:
            screen_resolution = out.strip()

        screen_depth = ""
        cmd = ["cat", "/sys/class/graphics/fb0/bits_per_pixel"]
        out, err = self.execute_cmd(cmd)

        if err:
            # print("Error trying to read output devices:%s" % (err,))
            pass
        else:
            screen_depth = out.strip()

        if not (screen_name == "" and screen_resolution == ""):
            self.screens = [
                {
                    "name": screen_name,
                    "resolution": screen_resolution,
                    "pel_size": screen_depth,
                    "extra": "",
                }
            ]

        capabilities = {
            "keyboards": self.keyboards,
            "mice": self.mice,
            "screens": self.screens,
        }
        return capabilities


    def get_serial_number(self):
        cmd = "cat /proc/cpuinfo | grep Serial"
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=None, shell=True)
        output = process.communicate()[0] 
        if output:
            output = output.decode('utf-8')
            self.pi_serial_number = output.split(":")[1]
        return self.pi_serial_number


    def cpu_is_pi4(self):
        result = False
        cmd = "cat /proc/cpuinfo | grep Model"
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=None, shell=True)
        output = process.communicate()[0] 
        if output:
            output = output.decode('utf-8')
            if output.find("Raspberry Pi 4") > -1:
                result = True
                self.get_serial_number() 
        return result


    def get_memory_size(self):
        mem_size = 0
        cmd = "grep MemTotal /proc/meminfo"
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=None, shell=True)
        output = process.communicate()[0]
        if output:
            output = output.decode('utf-8')
            mem_size = output.split(" ")[-2:-1][0]

        return mem_size


    def get_storage_info(self):       
        disk_total = 0
        disk_available = 0
        cmd = "df -h | grep root"
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=None, shell=True)
        output = process.communicate()[0]
        if output:
            output = output.decode('utf-8')
            while output.find("  ") > -1:
                output = output.replace("  ", " ")
            output = output.split(" ")
            disk_total = output[1]
            disk_available = output[3]

        return disk_total, disk_available



##########
## Main ##
##########
if __name__ == "__main__":
    """
    try to auto detect a markii
    we want to know about any keyboards,
    mice, and screens attached to the system.

    currently a markii has the following 
    distinguishing characteristics ...

    1) CPU is a Pi4
    2) Has 2GB of Memory
    3) Has a 16GB USB drive
    4) Has a Touch Screen with a resolution of 800x480


    """
    hc = EnclosureCapabilities()

    touch_screen = 'Fail'
    memory = 'Fail'
    storage = 'Fail'

    if hc.mice[0]['name'] == 'raspberrypi-ts' and hc.screens[0]['name'] == 'vc4drmfb':
        res = hc.screens[0]['resolution']
        res = res.replace(",", " by ")
        print("Touch screen found - resolution is %s" % (res,))
        #os.system("aplay wavs/touch_screen_found.wav")
        touch_screen = 'Pass'
    else:
        print("Error - touch screen NOT found!")
        #os.system("aplay wavs/no_touch_screen.wav")

    mem_size = hc.get_memory_size()
    if mem_size != '1892728':
        print("Error - unexpected memory size = %s" % (output,))
        #os.system("aplay wavs/memory_bad.wav")
    else:
        print("Memory size = %s kb" % (mem_size,))
        #os.system("aplay wavs/memory_good.wav")
        memory = 'Pass'

    if hc.cpu_is_pi4():
        print("CPU == MarkII")
    else:
        print("CPU <> MarkII")

    disk_total, disk_available = hc.get_storage_info()
    if disk_total != "14G":
        print("Warning, storage does not look like a Mark two.")
        #os.system("aplay wavs/storage_bad.wav")
    else:
        print("Storage looks like this is a Mark two.")
        #os.system("aplay wavs/storage_good.wav")
        storage = 'Pass'

    print("Touch Screen: %s" % (touch_screen,))
    print("Memory: %s" % (memory,))
    print("Total Disk Storage: %s, Available Disk Storage: %s" % (disk_total,disk_available))

