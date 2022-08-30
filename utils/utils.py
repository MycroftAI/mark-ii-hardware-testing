import os
import time

# print colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color


def fix_cmd(board_type, usr_cmd):
    # can't run certain stuff as sudo
    # so we handle that here
    cmd = usr_cmd
    if board_type == 2:
        cmd = "su pi -c '" + usr_cmd + "'"
    os.system(cmd)


class CommandExecutor:
    """
    Support for old school type linux utilities 
    like aplay and mpg123. Note, for async users,
    mpg123 should be terminated using send('s')
    while aplay requires kill(). Note also you
    can not currently read stdout using this 
    method. 
    Synchronous Example:
      retcode = CommandExecutor('aplay -i test.wav').wait()
    Asynchronous Example:
      ce = CommandExecutor('aplay -i test.wav')
      ce.send(' ')  # pause aplay or send 's' to pause mpg123
      ce.kill()     # stop play or send 'q' to kill mpg123
    """
    def __init__(self, command):
        self.error = None
        self.proc = None
        self.master = None
        self.slave = None
        self.master, self.slave = os.openpty()
        try:
            self.proc = Popen(command.strip().split(" "), stdin=self.master)
        except Exception as e:
            self.error = e

        time.sleep(0.0625)     # if you write too fast you hose the fd

    def send(self, text):
        os.write(self.slave, text.encode('utf-8'))

    def is_completed(self):
        # call this and when it returns true 
        # you can call get_return_code()
        try:
            if self.proc.poll() is None:
                return False
            else:
                return True
        except:
            return True

    def get_return_code(self):
        # if None, still alive 
        if self.proc is not None:
            return self.proc.returncode
        return self.proc

    def kill(self):
        if self.proc:
            self.proc.kill()
        os.close(self.slave)
        os.close(self.master)

    def wait(self):
        print("CMD EXEC WAIT()! XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        while not self.is_completed():
            time.sleep(1)
        print("CMD EXEC END WAIT()! XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        return self.get_return_code()


class LogicalVolume:
    def __init__(self, leds, board_type):
        self.leds = leds
        self.board_type = board_type
        self.vol_table = [180,170,160,150,140,130,120,110,100,90,80,70]
        self.current_volume = 6 # index into vol table
        cmd = "python utils/set_volume_tas5806.py %s" % (self.vol_table[self.current_volume],)
        fix_cmd(self.board_type, cmd)

    def vol_up(self):
        self.leds._set_led(self.current_volume, (255,0,0))
        self.current_volume += 1
        if self.current_volume > 11:
            self.current_volume = 11
        cmd = "python utils/set_volume_tas5806.py %s" % (self.vol_table[self.current_volume],)
        fix_cmd(self.board_type, cmd)

    def vol_down(self):
        self.current_volume -= 1
        if self.current_volume < 0:
            self.current_volume = 0
        self.leds._set_led(self.current_volume, (0,0,0))
        cmd = "python utils/set_volume_tas5806.py %s" % (self.vol_table[self.current_volume],)
        fix_cmd(self.board_type, cmd)

    def close(self):
        pass


