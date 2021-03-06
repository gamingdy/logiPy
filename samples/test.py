import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


from logipy.logi_led import NotImplemented, LogitechLed
import time
import ctypes
import random


print("Initialize...")
logi_led = LogitechLed()
b = logi_led.pulse_lighting(50, 100, 0, 0, 500)
time.sleep(5)
logi_led_test = NotImplemented()

b = logi_led_test.stop_effects()

input("Press enter to shutdown SDK...")
logi_led.shutdown()
# logi_led_test.shutdown()
