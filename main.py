import time
import board
import digitalio
import usb_hid
import busio
import displayio
import terminalio
from adafruit_display_text import label
from i2cdisplaybus import I2CDisplayBus
from adafruit_displayio_ssd1306 import SSD1306

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

displayio.release_displays()

i2c = busio.I2C(scl=board.GP5, sda=board.GP4)

display_bus = I2CDisplayBus(i2c, device_address=0x3C)
display = SSD1306(display_bus, width=128, height=64)

splash = displayio.Group()
display.root_group = splash

text = "Macro Keyboard"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=10, y=15)
splash.append(text_area)

keyboard = Keyboard(usb_hid.devices)
consumer_control = ConsumerControl(usb_hid.devices)

btn0_pin = board.GP15

btn0 = digitalio.DigitalInOut(btn0_pin)
btn0.direction = digitalio.Direction.INPUT
btn0.pull = digitalio.Pull.DOWN

btn1_pin = board.GP14

btn1 = digitalio.DigitalInOut(btn1_pin)
btn1.direction = digitalio.Direction.INPUT
btn1.pull = digitalio.Pull.DOWN

btn2_pin = board.GP13

btn2 = digitalio.DigitalInOut(btn2_pin)
btn2.direction = digitalio.Direction.INPUT
btn2.pull = digitalio.Pull.DOWN

btn3_pin = board.GP12

btn3 = digitalio.DigitalInOut(btn3_pin)
btn3.direction = digitalio.Direction.INPUT
btn3.pull = digitalio.Pull.DOWN

btn4_pin = board.GP11

btn4 = digitalio.DigitalInOut(btn4_pin)
btn4.direction = digitalio.Direction.INPUT
btn4.pull = digitalio.Pull.DOWN

btn0_prev = False
btn1_prev = False
btn2_prev = False
btn3_prev = False
btn4_prev = False

while True:
    if btn0.value and not btn0_prev:
        consumer_control.press(ConsumerControlCode.SCAN_PREVIOUS_TRACK)
    elif not btn0.value and btn0_prev:
        consumer_control.release()
    btn0_prev = btn0.value

    if btn1.value and not btn1_prev:
        consumer_control.press(ConsumerControlCode.PLAY_PAUSE)
    elif not btn1.value and btn1_prev:
        consumer_control.release()
    btn1_prev = btn1.value

    if btn2.value and not btn2_prev:
        consumer_control.press(ConsumerControlCode.SCAN_NEXT_TRACK)
    elif not btn2.value and btn2_prev:
        consumer_control.release()
    btn2_prev = btn2.value

    if btn3.value and not btn3_prev:
        consumer_control.press(ConsumerControlCode.VOLUME_DECREMENT)
    elif not btn3.value and btn3_prev:
        consumer_control.release()
    btn3_prev = btn3.value

    if btn4.value and not btn4_prev:
        consumer_control.press(ConsumerControlCode.VOLUME_INCREMENT)
    elif not btn4.value and btn4_prev:
        consumer_control.release()
    btn4_prev = btn4.value
        
    time.sleep(0.1)