# Copyright 2020 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import time
import board
import neopixel
from MycroftLed import MycroftLed

class Led(MycroftLed):
    led_type = 'new'
    real_num_leds = 12  # physical
    num_leds = 10  # logical
    black = (0, 0, 0)  # TODO pull from pallette

    def __init__(self):
        pixel_pin = board.D12
        ORDER = neopixel.GRB
        self.brightness = 0.2

        self.pixels = neopixel.NeoPixel(
            pixel_pin,
            self.real_num_leds,
            brightness=self.brightness,
            auto_write=False,
            pixel_order=ORDER
        )

        self.capabilities = {
            "num_leds": self.num_leds,
            "brightness": "(0.0-1.0)",
            "led_colors": "MycroftPalette",
            "reserved_leds": list(range(self.num_leds, self.real_num_leds)),
        }

    def adjust_brightness(self, cval, bval):
        return min(255, cval * bval)

    def get_capabilities(self):
        return self.capabilities

    def _set_led(self, pixel, color):
        """internal interface
        permits access to the
        reserved leds"""
        red_val = int(color[0])
        green_val = int(color[1])
        blue_val = int(color[2])
        self.pixels[pixel] = (red_val, green_val, blue_val)

    def _set_led_with_brightness(self, pixel, color, blevel):
        self._set_led(pixel, list(map(self.adjust_brightness, color, (blevel,) * 3)))

    def show(self):
        """show buffered leds, only used
        for older slower devices"""
        self.pixels.show()

    def set_led(self, pixel, color):
        """external interface enforces led
        reservation and honors brightness"""
        self._set_led(
            pixel % self.num_leds,
            list(map(self.adjust_brightness, color, (self.brightness,) * 3)),
        )

    def fill(self, color):
        """fill all leds with the same color"""
        rgb = [int(self.adjust_brightness(c, self.brightness)) for c in color[:3]]
        self.pixels.fill(rgb)
        self.pixels.show()


    def set_leds(self, new_leds):
        """set leds from tuple array"""
        for x in range(0, self.num_leds):
            self.set_led(x, new_leds[x])

if __name__ == "__main__":
    print("Starting Brightness Test")
    leds = Led()
    leds.fill((0,0,0))

    colors = [(255,0,0), (255,0,0), (255,0,0)]
    color_index = 0
    while color_index < 1:
        fill_color = colors[color_index]
        leds.brightness = 0.0
        while leds.brightness < 1.0:
            time.sleep(0.125)
            leds.fill(fill_color)
            leds.brightness += 0.1

        while leds.brightness > 0.0:
            time.sleep(0.125)
            leds.fill(fill_color)
            leds.brightness -= 0.1

        color_index += 1

    print("Brightness Test Completed")

