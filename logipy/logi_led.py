"""
logi_led.py : Defines the exported functions for the API
Logitech Gaming LED SDK
Copyright (C) 2011-2015 Logitech. All rights reserved.
Original author: Tom Lambert
Email: devtechsupport@logitech.com
"""

"""
This is a fork of https://github.com/Logitech/logiPy 
by gamingdy
"""

import ctypes
import os
import platform
import struct
from pathlib import Path


# DLL Definitions
#
ESC = 0x01
F1 = 0x3B
F2 = 0x3C
F3 = 0x3D
F4 = 0x3E
F5 = 0x3F
F6 = 0x40
F7 = 0x41
F8 = 0x42
F9 = 0x43
F10 = 0x44
F11 = 0x57
F12 = 0x58
PRINT_SCREEN = 0x137
SCROLL_LOCK = 0x46
PAUSE_BREAK = 0x145
TILDE = 0x29
ONE = 0x02
TWO = 0x03
THREE = 0x04
FOUR = 0x05
FIVE = 0x06
SIX = 0x07
SEVEN = 0x08
EIGHT = 0x09
NINE = 0x0A
ZERO = 0x0B
MINUS = 0x0C
EQUALS = 0x0D
BACKSPACE = 0x0E
INSERT = 0x152
HOME = 0x147
PAGE_UP = 0x149
NUM_LOCK = 0x45
NUM_SLASH = 0x135
NUM_ASTERISK = 0x37
NUM_MINUS = 0x4A
TAB = 0x0F
Q = 0x10
W = 0x11
E = 0x12
R = 0x13
T = 0x14
Y = 0x15
U = 0x16
I = 0x17
O = 0x18
P = 0x19
OPEN_BRACKET = 0x1A
CLOSE_BRACKET = 0x1B
BACKSLASH = 0x2B
KEYBOARD_DELETE = 0x153
END = 0x14F
PAGE_DOWN = 0x151
NUM_SEVEN = 0x47
NUM_EIGHT = 0x48
NUM_NINE = 0x49
NUM_PLUS = 0x4E
CAPS_LOCK = 0x3A
A = 0x1E
S = 0x1F
D = 0x20
F = 0x21
G = 0x22
H = 0x23
J = 0x24
K = 0x25
L = 0x26
SEMICOLON = 0x27
APOSTROPHE = 0x28
ENTER = 0x1C
NUM_FOUR = 0x4B
NUM_FIVE = 0x4C
NUM_SIX = 0x4D
LEFT_SHIFT = 0x2A
Z = 0x2C
X = 0x2D
C = 0x2E
V = 0x2F
B = 0x30
N = 0x31
M = 0x32
COMMA = 0x33
PERIOD = 0x34
FORWARD_SLASH = 0x35
RIGHT_SHIFT = 0x36
ARROW_UP = 0x148
NUM_ONE = 0x4F
NUM_TWO = 0x50
NUM_THREE = 0x51
NUM_ENTER = 0x11C
LEFT_CONTROL = 0x1D
LEFT_WINDOWS = 0x15B
LEFT_ALT = 0x38
SPACE = 0x39
RIGHT_ALT = 0x138
RIGHT_WINDOWS = 0x15C
APPLICATION_SELECT = 0x15D
RIGHT_CONTROL = 0x11D
ARROW_LEFT = 0x14B
ARROW_DOWN = 0x150
ARROW_RIGHT = 0x14D
NUM_ZERO = 0x52
NUM_PERIOD = 0x53
G_1 = 0xFFF1
G_2 = 0xFFF2
G_3 = 0xFFF3
G_4 = 0xFFF4
G_5 = 0xFFF5
G_6 = 0xFFF6
G_7 = 0xFFF7
G_8 = 0xFFF8
G_9 = 0xFFF9
G_LOGO = 0xFFFF1
G_BADGE = 0xFFFF2

LOGI_LED_BITMAP_WIDTH = 21
LOGI_LED_BITMAP_HEIGHT = 6
LOGI_LED_BITMAP_BYTES_PER_KEY = 4

LOGI_LED_BITMAP_SIZE = (
    LOGI_LED_BITMAP_WIDTH * LOGI_LED_BITMAP_HEIGHT * LOGI_LED_BITMAP_BYTES_PER_KEY
)

LOGI_LED_DURATION_INFINITE = 0

LOGI_DEVICETYPE_MONOCHROME_ORD = 0
LOGI_DEVICETYPE_RGB_ORD = 1
LOGI_DEVICETYPE_PERKEY_RGB_ORD = 2

LOGI_DEVICETYPE_MONOCHROME = 1 << LOGI_DEVICETYPE_MONOCHROME_ORD
LOGI_DEVICETYPE_RGB = 1 << LOGI_DEVICETYPE_RGB_ORD
LOGI_DEVICETYPE_PERKEY_RGB = 1 << LOGI_DEVICETYPE_PERKEY_RGB_ORD

LOGI_DEVICETYPE_ALL = (
    LOGI_DEVICETYPE_MONOCHROME | LOGI_DEVICETYPE_RGB | LOGI_DEVICETYPE_PERKEY_RGB
)


# Required Globals
#
_LOGI_SHARED_SDK_LED = ctypes.c_int(1)


class SDKNotFoundException(BaseException):
    pass


class LGHUBNotLaunched(BaseException):
    pass


# Helpers
#
class Color:
    """an RGBA color object that can be created using RGB, RGBA, color name, or a hex_code."""

    def __init__(self, *args, **kwargs):
        red, green, blue, alpha = 0, 0, 0, 255
        hex_code = None
        if len(args) > 0:
            if isinstance(args[0], int):
                red, green, blue = args[0], args[1], args[2]
                if len(args) > 3:
                    alpha = args[3]
            elif isinstance(args[0], str):
                if len(args) > 1:
                    alpha = args[1]
                if args[0] == "red":
                    red, green, blue = 255, 0, 0
                elif args[0] == "orange":
                    red, green, blue = 255, 165, 0
                elif args[0] == "yellow":
                    red, green, blue = 255, 255, 0
                elif args[0] == "green":
                    red, green, blue = 0, 255, 0
                elif args[0] == "blue":
                    red, green, blue = 0, 0, 255
                elif args[0] == "indigo":
                    red, green, blue = 75, 0, 130
                elif args[0] == "violet":
                    red, green, blue = 238, 130, 238
                elif args[0] == "cyan":
                    red, green, blue = 0, 220, 255
                elif args[0] == "pink":
                    red, green, blue = 255, 0, 255
                elif args[0] == "purple":
                    red, green, blue = 128, 0, 255
                elif args[0] == "white":
                    red, green, blue = 255, 255, 255
                elif args[0] == "black":
                    red, green, blue = 0, 0, 0
                else:
                    hex_code = args[0]
                    hex_code = kwargs.pop("hex", hex_code)
        if hex_code:
            hex_code = hex_code.replace("#", "")
            self.red, self.green, self.blue = struct.unpack(
                "BBB", hex_code.decode("hex")
            )
            self.alpha = alpha
        elif any(x in ["red", "blue", "green", "alpha"] for x in kwargs):
            self.red = kwargs.pop("red", red)
            self.green = kwargs.pop("green", green)
            self.blue = kwargs.pop("blue", blue)
            self.alpha = kwargs.pop("alpha", alpha)
        else:
            self.red = red
            self.green = green
            self.blue = blue
            self.alpha = alpha
        self.hex_code = "#{h}".format(
            h=struct.pack("BBB", *(self.red, self.green, self.blue)).encode("hex")
        )

    def rgb_percent(self):
        return (
            int((self.red / 255.0) * 100),
            int((self.green / 255.0) * 100),
            int((self.blue / 255.0) * 100),
        )


class LogitechLed:
    def __init__(self):
        self._initialize_led()

    def _load_dll(self):
        prev_cwd = Path(__file__).parent
        path_dll = f"{prev_cwd}/dll/LogitechLedEnginesWrapper.dll"
        if os.path.exists(path_dll):
            return ctypes.cdll.LoadLibrary(path_dll)
        else:
            raise SDKNotFoundException("The SDK DLL was not found.")

    def _initialize_led(self):
        """initializes the sdk for the current thread."""
        self.led_dll = self._load_dll()
        if not bool(self.led_dll.LogiLedInit()):
            raise LGHUBNotLaunched(
                "You must start Logitech GHUB before using the Logipy packages"
            )

    def logi_led_shutdown(self):
        """shutdowns the SDK for the thread."""
        return bool(self.led_dll.LogiLedShutdown())

    def logi_led_set_lighting_for_target_zone(
        zone=0,
        red_percentage=0,
        green_percentage=0,
        blue_percentage=0,
    ):
        """
        Set lighting for specific zone
        """
        return self.led_dll.LogiLedSetLightingForTargetZone(
            None, zone, red_percentage, green_percentage, blue_percentage
        )


def logi_led_set_target_device(target_device):
    """sets the target device or device group that is affected by the subsequent lighting calls."""
    if led_dll:
        target_device = ctypes.c_int(target_device)
        return bool(led_dll.LogiLedSetTargetDevice(target_device))
    else:
        return False


def logi_led_save_current_lighting():
    """saves the current lighting that can be restored later."""
    if led_dll:
        return bool(led_dll.LogiLedSaveCurrentLighting())
    else:
        return False


def logi_led_restore_lighting():
    """restores the last saved lighting."""
    if led_dll:
        return bool(led_dll.LogiLedRestoreLighting())
    else:
        return False


def logi_led_set_lighting(red_percentage, green_percentage, blue_percentage):
    """sets the lighting to the color of the combined RGB percentages. note that RGB ranges from 0-255, but this function ranges from 0-100."""
    if led_dll:
        red_percentage = ctypes.c_int(red_percentage)
        green_percentage = ctypes.c_int(green_percentage)
        blue_percentage = ctypes.c_int(blue_percentage)
        return bool(
            led_dll.LogiLedSetLighting(
                red_percentage, green_percentage, blue_percentage
            )
        )
    else:
        return False


def logi_led_flash_lighting(
    red_percentage, green_percentage, blue_percentage, ms_duration, ms_interval
):
    """flashes the lighting color of the combined RGB percentages over the specified millisecond duration and millisecond interval.
    specifying a duration of 0 will cause the effect to be infinite until reset. note that RGB ranges from 0-255, but this function ranges from 0-100."""
    if led_dll:
        red_percentage = ctypes.c_int(red_percentage)
        green_percentage = ctypes.c_int(green_percentage)
        blue_percentage = ctypes.c_int(blue_percentage)
        ms_duration = ctypes.c_int(ms_duration)
        ms_interval = ctypes.c_int(ms_interval)
        return bool(
            led_dll.LogiLedFlashLighting(
                red_percentage,
                green_percentage,
                blue_percentage,
                ms_duration,
                ms_interval,
            )
        )
    else:
        return False


def logi_led_pulse_lighting(
    red_percentage, green_percentage, blue_percentage, ms_duration, ms_interval
):
    """pulses the lighting color of the combined RGB percentages over the specified millisecond duration and millisecond interval.
    specifying a duration of 0 will cause the effect to be infinite until reset. note that RGB ranges from 0-255, but this function ranges from 0-100."""
    if led_dll:
        red_percentage = ctypes.c_int(red_percentage)
        green_percentage = ctypes.c_int(green_percentage)
        blue_percentage = ctypes.c_int(blue_percentage)
        ms_duration = ctypes.c_int(ms_duration)
        ms_interval = ctypes.c_int(ms_interval)
        return bool(
            led_dll.LogiLedPulseLighting(
                red_percentage,
                green_percentage,
                blue_percentage,
                ms_duration,
                ms_interval,
            )
        )
    else:
        return False


def logi_led_stop_effects():
    """stops the pulse and flash effects."""
    if led_dll:
        return bool(led_dll.LogiLedStopEffects())
    else:
        return False


def logi_led_set_lighting_from_bitmap(bitmap):
    """sets the color of each key in a 21x6 rectangular area specified by the BGRA byte array bitmap. each element corresponds to the physical location of each key.
    note that the color bit order is BGRA rather than standard RGBA bit order. this function only applies to LOGI_DEVICETYPE_PERKEY_RGB devices."""
    if led_dll:
        bitmap = ctypes.c_char_p(bitmap)
        return bool(led_dll.LogiLedSetLightingFromBitmap(bitmap))
    else:
        return False


def logi_led_set_lighting_for_key_with_scan_code(
    key_code, red_percentage, green_percentage, blue_percentage
):
    """sets the lighting to the color of the combined RGB percentages for the specified key code. note that RGB ranges from 0-255, but this function ranges from 0-100.
    this function only applies to LOGI_DEVICETYPE_PERKEY_RGB devices."""
    if led_dll:
        key_code = ctypes.c_int(key_code)
        red_percentage = ctypes.c_int(red_percentage)
        green_percentage = ctypes.c_int(green_percentage)
        blue_percentage = ctypes.c_int(blue_percentage)
        return bool(
            led_dll.LogiLedSetLightingForKeyWithScanCode(
                key_code, red_percentage, green_percentage, blue_percentage
            )
        )
    else:
        return False


def logi_led_set_lighting_for_key_with_hid_code(
    key_code, red_percentage, green_percentage, blue_percentage
):
    """sets the lighting to the color of the combined RGB percentages for the specified key code. note that RGB ranges from 0-255, but this function ranges from 0-100.
    this function only applies to LOGI_DEVICETYPE_PERKEY_RGB devices."""
    if led_dll:
        key_code = ctypes.c_int(key_code)
        red_percentage = ctypes.c_int(red_percentage)
        green_percentage = ctypes.c_int(green_percentage)
        blue_percentage = ctypes.c_int(blue_percentage)
        return bool(
            led_dll.LogiLedSetLightingForKeyWithHidCode(
                key_code, red_percentage, green_percentage, blue_percentage
            )
        )
    else:
        return False


def logi_led_set_lighting_for_key_with_quartz_code(
    key_code, red_percentage, green_percentage, blue_percentage
):
    """sets the lighting to the color of the combined RGB percentages for the specified key code. note that RGB ranges from 0-255, but this function ranges from 0-100.
    this function only applies to LOGI_DEVICETYPE_PERKEY_RGB devices."""
    if led_dll:
        key_code = ctypes.c_int(key_code)
        red_percentage = ctypes.c_int(red_percentage)
        green_percentage = ctypes.c_int(green_percentage)
        blue_percentage = ctypes.c_int(blue_percentage)
        return bool(
            led_dll.LogiLedSetLightingForKeyWithQuartzCode(
                key_code, red_percentage, green_percentage, blue_percentage
            )
        )
    else:
        return False


def logi_led_set_lighting_for_key_with_key_name(
    key_name, red_percentage, green_percentage, blue_percentage
):
    """sets the lighting to the color of the combined RGB percentages for the specified key name. note that RGB ranges from 0-255, but this function ranges from 0-100.
    this function only applies to LOGI_DEVICETYPE_PERKEY_RGB devices."""
    if led_dll:
        key_name = ctypes.c_int(key_name)
        red_percentage = ctypes.c_int(red_percentage)
        green_percentage = ctypes.c_int(green_percentage)
        blue_percentage = ctypes.c_int(blue_percentage)
        return bool(
            led_dll.LogiLedSetLightingForKeyWithKeyName(
                key_name, red_percentage, green_percentage, blue_percentage
            )
        )
    else:
        return False


def logi_led_save_lighting_for_key(key_name):
    """saves the current lighting for the specified key name that can be restored later. this function only applies to LOGI_DEVICETYPE_PERKEY_RGB devices."""
    if led_dll:
        key_name = ctypes.c_int(key_name)
        return bool(led_dll.LogiLedSaveLightingForKey(key_name))
    else:
        return False


def logi_led_restore_lighting_for_key(key_name):
    """restores the last saved lighting for the specified key name. this function only applies to LOGI_DEVICETYPE_PERKEY_RGB devices."""
    if led_dll:
        key_name = ctypes.c_int(key_name)
        return bool(led_dll.LogiLedRestoreLightingForKey(key_name))
    else:
        return False


def logi_led_flash_single_key(
    key_name,
    red_percentage,
    green_percentage,
    blue_percentage,
    ms_duration,
    ms_interval,
):
    """flashes the lighting color of the combined RGB percentages over the specified millisecond duration and millisecond interval for the specified key name.
    specifying a duration of 0 will cause the effect to be infinite until reset. note that RGB ranges from 0-255, but this function ranges from 0-100.
    this function only applies to LOGI_DEVICETYPE_PERKEY_RGB devices."""
    if led_dll:
        key_name = ctypes.c_int(key_name)
        red_percentage = ctypes.c_int(red_percentage)
        green_percentage = ctypes.c_int(green_percentage)
        blue_percentage = ctypes.c_int(blue_percentage)
        ms_duration = ctypes.c_int(ms_duration)
        ms_interval = ctypes.c_int(ms_interval)
        return bool(
            led_dll.LogiLedFlashSingleKey(
                key_name,
                red_percentage,
                green_percentage,
                blue_percentage,
                ms_duration,
                ms_interval,
            )
        )
    else:
        return False


def logi_led_pulse_single_key(
    key_name,
    red_percentage_start,
    green_percentage_start,
    blue_percentage_start,
    ms_duration,
    is_infinite=False,
    red_percentage_end=0,
    green_percentage_end=0,
    blue_percentage_end=0,
):
    """pulses the lighting color of the combined RGB percentages over the specified millisecond duration for the specified key name.
    the color will gradually change from the starting color to the ending color. if no ending color is specified, the ending color will be black.
    the effect will stop after one interval unless is_infinite is set to True. note that RGB ranges from 0-255, but this function ranges from 0-100.
    this function only applies to LOGI_DEVICETYPE_PERKEY_RGB devices."""
    if led_dll:
        key_name = ctypes.c_int(key_name)
        red_percentage_start = ctypes.c_int(red_percentage_start)
        green_percentage_start = ctypes.c_int(green_percentage_start)
        blue_percentage_start = ctypes.c_int(blue_percentage_start)
        red_percentage_end = ctypes.c_int(red_percentage_end)
        green_percentage_end = ctypes.c_int(green_percentage_end)
        blue_percentage_end = ctypes.c_int(blue_percentage_end)
        ms_duration = ctypes.c_int(ms_duration)
        is_infinite = ctypes.c_bool(is_infinite)
        return bool(
            led_dll.LogiLedPulseSingleKey(
                key_name,
                red_percentage_start,
                green_percentage_start,
                blue_percentage_start,
                red_percentage_end,
                green_percentage_end,
                blue_percentage_end,
                ms_duration,
                is_infinite,
            )
        )
    else:
        return False


def logi_led_stop_effects_on_key(key_name):
    """stops the pulse and flash effects on a single key."""
    if led_dll:
        key_name = ctypes.c_int(key_name)
        return bool(led_dll.LogiLedStopEffectsOnKey(key_name))
    else:
        return False


def logi_led_get_config_option_number(key, default=0):
    """get the default value for the key as a number. if the call fails, the return value is None.
    for example, get the low health threshold:
     logi_led_get_config_option_number('health/low_health_threshold', 20.0)"""
    if led_dll:
        key = ctypes.c_wchar_p(key)
        default = ctypes.c_double(default)
        if led_dll.LogiGetConfigOptionNumber(
            key, ctypes.pointer(default), _LOGI_SHARED_SDK_LED
        ):
            return default.value
    return None


def logi_led_get_config_option_bool(key, default=False):
    """get the default value for the key as a bool. if the call fails, the return value is None.
    for example, check if the effect is enabled:
     logi_led_get_config_option_bool('health/pulse_on_low', True)"""
    if led_dll:
        key = ctypes.c_wchar_p(key)
        default = ctypes.c_bool(default)
        if led_dll.LogiGetConfigOptionBool(
            key, ctypes.pointer(default), _LOGI_SHARED_SDK_LED
        ):
            return default.value
    return None


def logi_led_get_config_option_color(key, *args):
    """get the default value for the key as a color. if the call fails, the return value is None.
     note this function can either be called with red_percentage, green_percentage, and blue_percentage or with the logi_led Color object.
    for example, get the low health color:
     logi_led_get_config_option_color('health/pulse_color', 100, 0, 0)
     logi_led_get_config_option_color('health/pulse_color', Color('red'))
     logi_led_get_config_option_color('health/pulse_color', Color('#ff0000'))
     logi_led_get_config_option_color('health/pulse_color', Color(255, 0, 0))"""
    if led_dll:
        key = ctypes.c_wchar_p(key)
        default = None
        red_percentage = 0
        green_percentage = 0
        blue_percentage = 0
        if isinstance(args[0], Color):
            default = args[0]
        else:
            red_percentage = args[0]
            green_percentage = args[1]
            blue_percentage = args[2]
        if default:
            red = ctypes.c_int(default.red)
            green = ctypes.c_int(default.green)
            blue = ctypes.c_int(default.blue)
        else:
            red = ctypes.c_int(int((red_percentage / 100.0) * 255))
            green = ctypes.c_int(int((green_percentage / 100.0) * 255))
            blue = ctypes.c_int(int((blue_percentage / 100.0) * 255))
        if led_dll.LogiGetConfigOptionColor(
            key,
            ctypes.pointer(red),
            ctypes.pointer(green),
            ctypes.pointer(blue),
            _LOGI_SHARED_SDK_LED,
        ):
            return Color(red.value, green.value, blue.value)
    return None


def logi_led_get_config_option_key_input(key, default=""):
    """get the default value for the key as a key input. if the call fails, the return value is None.
    for example, get the primary ability key input:
     logi_led_get_config_option_key_input('abilities/primary', 'A')"""
    if led_dll:
        key = ctypes.c_wchar_p(key)
        default_key = ctypes.create_string_buffer(256)
        default_key.value = default
        if led_dll.LogiGetConfigOptionKeyInput(key, default_key, _LOGI_SHARED_SDK_LED):
            return str(default_key.value)
    return None


def logi_led_set_config_option_label(key, label):
    """set the label for a key.
    for example, label 'health/pulse_on_low' as 'Health - Pulse on Low':
     logi_led_set_config_option_label('health', 'Health')
     logi_led_set_config_option_label('health/pulse_on_low', 'Pulse on Low')"""
    if led_dll:
        key = ctypes.c_wchar_p(key)
        label = ctypes.c_wchar_p(label)
        return bool(led_dll.LogiSetConfigOptionLabel(key, label, _LOGI_SHARED_SDK_LED))
    else:
        return False
