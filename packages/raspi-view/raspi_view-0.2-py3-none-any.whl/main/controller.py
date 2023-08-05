from enum import Enum
from time import sleep
from gpiozero import PWMLED, Button
from PIL import ImageDraw

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106

class Controller(object):
    def __init__(self, push_handler, port=1, address=0x3C):
        self.led_red = PWMLED(6)
        self.led_blue = PWMLED(12)
        self._red_count = 0
        self._blue_count = 0

        self.button_left = Button(5)
        self.button_right = Button(21)

        self.button_left.when_activated = push_handler

        serial = i2c(port=port, address=address)
        self.device = sh1106(serial)

        self._test_outputs()

    def get_canvas(self) -> ImageDraw:
        return canvas(self.device) 

    def get_device_bounding_box(self) -> list:
        return self.device.bounding_box

    def flash(self, red_count=0, blue_count=0):
        self._flash(self.led_red, red_count, self._red_count)
        self._red_count = red_count
        self._flash(self.led_blue, blue_count, self._blue_count)
        self._blue_count = blue_count

    def _flash(self, led: PWMLED, new_count=0, old_count=0):
        if new_count is not old_count:
            if new_count > 0:
                time = 2.0 / min(new_count, 20)
                led.blink(on_time=time, off_time=time)
            else:
                led.off()

    def _test_outputs(self):
        print("testing outputs for one second...")

        self.led_blue.on()
        self.led_red.on()

        box = self.get_device_bounding_box()
        with self.get_canvas() as canvas:
            canvas.rectangle(box, outline="white", fill="black")
            canvas.ellipse((1, 1, box[2], box[3]), outline="white")
            canvas.line(box, fill="white")
            canvas.line((0, box[3], box[2], 0), fill="white")

        sleep(1)

        self.led_blue.off()
        self.led_red.off()

        with self.get_canvas() as canvas:
            canvas.rectangle(self.get_device_bounding_box(), fill="black")
        