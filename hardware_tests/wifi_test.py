from subprocess import Popen, PIPE

def run_cmd(cmd, type_flag, key):
    err = True
    process = Popen(cmd, stdout=PIPE, stderr=None, shell=True)
    output = process.communicate()[0]
    if output:
        output = output.decode('utf-8')
        lines = output.split("\n")
        for line in lines:
            if type_flag == "find":
                if line.find("Tx-Pow") > -1:
                    print("Transmit Power--->", line)
                    err=False
            else:
                if line.startswith("wlan0"):
                    print("Wifi Found--->", line)
                    err=False

    return err

if __name__ == "__main__":
    err = run_cmd("iwconfig wlan0", "find", "Tx-Pow")
    if err:
        print("Error finding transmit power")

    err = run_cmd("nmcli dev status | grep wlan0", "start", "wlan0")
    if err:
        print("Error finding device")

    err = run_cmd("ifconfig | grep wlan0", "start", "wlan0")
    if err:
        print("Error finding transmit power")

