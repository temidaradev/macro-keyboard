import time
import board
import digitalio

from adafruit_hid.keybaord import Keyboard
from adafruit_hid.keycode import Keycode

btn1_pin = board.GP15

btn1 = digitalio.DigitalInOut(btn1_pin)
btn1.direction = digitalio.Direction.INPUT
btn1.pull = digitalio.Pull.DOWN

while True:
    if btn1.value:
        print("Hello World")
        
    time.sleep(0.1)