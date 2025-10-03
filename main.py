import time
import board
import digitalio
import usb_hid
import busio
import displayio
from adafruit_display_text import label
from i2cdisplaybus import I2CDisplayBus
from adafruit_displayio_ssd1306 import SSD1306
from adafruit_bitmap_font import bitmap_font
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 64
DISPLAY_ADDRESS = 0x3C
I2C_SCL_PIN = board.GP5
I2C_SDA_PIN = board.GP4
FONT_FILE = "fonts/terminal.bdf"
BUTTON_PINS = [board.GP15, board.GP14, board.GP13, board.GP12, board.GP11]
DEBOUNCE_DELAY = 0.05

class Button:
    def __init__(self, pin):
        self.pin = digitalio.DigitalInOut(pin)
        self.pin.direction = digitalio.Direction.INPUT
        self.pin.pull = digitalio.Pull.DOWN
        self.previous_state = False
    
    @property
    def pressed(self):
        current = self.pin.value
        if current and not self.previous_state:
            return True
        return False
    
    @property
    def released(self):
        current = self.pin.value
        if not current and self.previous_state:
            return True
        return False
    
    def update(self):
        self.previous_state = self.pin.value


def setup_display():
    displayio.release_displays()
    
    i2c = busio.I2C(scl=I2C_SCL_PIN, sda=I2C_SDA_PIN)
    display_bus = I2CDisplayBus(i2c, device_address=DISPLAY_ADDRESS)
    display = SSD1306(display_bus, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT)
    
    font = bitmap_font.load_font(FONT_FILE)
    
    splash = displayio.Group()
    display.root_group = splash
    
    bg_bitmap = displayio.Bitmap(DISPLAY_WIDTH, DISPLAY_HEIGHT, 1)
    bg_palette = displayio.Palette(1)
    bg_palette[0] = 0xFFFFFF
    bg_sprite = displayio.TileGrid(bg_bitmap, pixel_shader=bg_palette, x=0, y=0)
    splash.append(bg_sprite)
    
    inner_bitmap = displayio.Bitmap(DISPLAY_WIDTH - 2, DISPLAY_HEIGHT - 2, 1)
    inner_palette = displayio.Palette(1)
    inner_palette[0] = 0x000000
    inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=1, y=1)
    splash.append(inner_sprite)
    
    title_label = label.Label(font, text="MACRO KEYBOARD", color=0xFFFFFF)
    title_label.anchor_point = (0.5, 0.0)
    title_label.anchored_position = (DISPLAY_WIDTH // 2, 5)
    splash.append(title_label)
    
    status_label = label.Label(font, text="READY", color=0xFFFFFF)
    status_label.anchor_point = (0.5, 0.5)
    status_label.anchored_position = (DISPLAY_WIDTH // 2, 38)
    status_label.scale = 3
    splash.append(status_label)
    
    return display, status_label

ACTIONS = [
    {"code": ConsumerControlCode.SCAN_PREVIOUS_TRACK, "label": "PREV"},
    {"code": ConsumerControlCode.PLAY_PAUSE, "label": "PLAY"},
    {"code": ConsumerControlCode.SCAN_NEXT_TRACK, "label": "NEXT"},
    {"code": ConsumerControlCode.VOLUME_DECREMENT, "label": "VOL-"},
    {"code": ConsumerControlCode.VOLUME_INCREMENT, "label": "VOL+"},
]

display, status_label = setup_display()
consumer_control = ConsumerControl(usb_hid.devices)
buttons = [Button(pin) for pin in BUTTON_PINS]
current_status = "READY"

last_action_time = 0
DISPLAY_TIMEOUT = 2.0

def update_status(new_status):
    global current_status, last_action_time
    if current_status != new_status:
        current_status = new_status
        status_label.text = current_status
        if new_status != "READY":
            last_action_time = time.monotonic()

print("Macro keyboard ready!")
while True:
    try:
        current_time = time.monotonic()
        
        if (current_status != "READY" and 
            current_time - last_action_time > DISPLAY_TIMEOUT):
            update_status("READY")
        
        for i, button in enumerate(buttons):
            action = ACTIONS[i]
            
            if button.pressed:
                consumer_control.press(action["code"])
                print(f"Button {i} pressed: {action['label']}")
            
            elif button.released:
                consumer_control.release()
                update_status(action["label"])  # Show action label
                print(f"Button {i} released: {action['label']}")
            
            button.update()
        
        time.sleep(DEBOUNCE_DELAY)
        
    except Exception as e:
        print(f"Error in main loop: {e}") 
        update_status("ERROR")
        time.sleep(0.5)