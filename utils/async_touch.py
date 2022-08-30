import asyncio
from asyncio.subprocess import PIPE
from asyncio import create_subprocess_exec
import subprocess 

"""
Wait for a touch event and exit
Can exit with success or time out
"""
class TouchEvent:
    process = None
    first = True
    got_key = False

    def __init__(self):
        # find the touch screen event 
        self.event_num = self.figure_out_which_event()


    def figure_out_which_event(self):
        evnt = 'event0'
        process = subprocess.Popen(
                'ls -l /dev/input',
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                shell=True,
                encoding='utf-8',
                errors='replace'
                )

        while True:
            output = process.stdout.readline()

            if output == '' and process.poll() is not None:
                break

            if output:
                line = output.strip()
                if line.find("event") > -1:
                    la = line.split(" ")
                    evnt = la[len(la)-1]

        return evnt


    async def _read_stream(self, stream, callback):
        while True:
            line = await stream.readline()
            if line:
                callback(line)
            else:
                break


    def handle_touch_event(self, l):
        l = l.decode("UTF8").strip()
        if l.find("EV_KEY") > -1:
            val = l.split(",")
            val = val[len(val)-1]
            if self.first:
                self.first = False
            else:
                self.got_key = True
                self.process.kill()


    async def run(self, command, timeout):
        self.process = await create_subprocess_exec(
            *command, stdout=PIPE, stderr=PIPE
        )

        await asyncio.wait(
            [
                self._read_stream(
                    self.process.stdout, self.handle_touch_event
                ),
                self._read_stream(
                    self.process.stderr,
                    lambda x: print(
                        "STDERR: {}".format(x.decode("UTF8"))
                    ),
                ),
            ], timeout=timeout
        )

        #await process.wait()
        print("run done")


    async def main(self):
        dev_id = "/dev/input/%s" % (self.event_num,)
        await self.run(["evtest", dev_id], 10)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    tse = TouchEvent()
    loop.run_until_complete(tse.main())
    print("main finished, got_key=%s" % (tse.got_key,))


