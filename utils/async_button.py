import asyncio
from asyncio.subprocess import PIPE
from asyncio import create_subprocess_exec
from time import sleep
from subprocess import Popen, PIPE
"""
Wait for one or more buttons
Can exit with success or time out
"""
class AsyncButtons:
    def __init__(self):
        self.got_key = False
        self.key_gpio = -1
        self.loop = asyncio.get_event_loop()

    async def _read_stream(self, stream, callback):
        while True:
            line = await stream.readline()
            if line:
                callback(line)
            else:
                break

    def handle_stderr(self, l):
        pass

    def handle_stdout(self, l):
        l = l.decode("UTF8").strip()
        tag = "level="
        if l.find(tag) > -1:
            indx = l.find(tag) + len(tag)
            val = int( l[indx:indx+1] )
            gpio = l.split(":")[0][5:]
            if val != 1:
                self.key_gpio = gpio
                self.got_key = True

    async def _wait_button(self, command):
        process = await create_subprocess_exec(
            *command, stdout=PIPE, stderr=PIPE
        )

        await asyncio.wait(
            [
                self._read_stream(process.stdout, self.handle_stdout),
                self._read_stream(process.stderr, self.handle_stderr),
            ]
        )

    async def _wait_buttons(self, buttons, timeout):
        self.got_key = False
        self.key_gpio = -1
        to_ctr = timeout * 50
        while not self.got_key and to_ctr:
            for button in buttons:
                await self._wait_button(["raspi-gpio","get", button])
            await asyncio.sleep(0.01)
            to_ctr -= 1

    def wait_buttons(self, buttons, timeout):
        self.loop.run_until_complete(self._wait_buttons(buttons, timeout))
        sleep(0.25)   # hard sleep to debounce
        return self.key_gpio

    def get_mic_switch(self):
        result = -1
        cmd = "raspi-gpio get 25"
        process = Popen(cmd, stdout=PIPE, stderr=None, shell=True)
        output = process.communicate()[0]
        if output:
            output = output.decode('utf-8')
            result = output[15:16]
        return result


if __name__ == "__main__":
    activate_button = '24'
    right_button = '22'
    middle_button = '23'
    m2but = AsyncButtons()

    while True:
        ms = m2but.get_mic_switch()
        print(ms)
        sleep(0.1)

    print("Any")
    buttons = [right_button, middle_button, activate_button]
    which = m2but.wait_buttons(buttons, 10)
    print(which)

    # only activate
    print("Only Activate")
    buttons = [activate_button,]
    which = m2but.wait_buttons(buttons, 5)
    print(which)

