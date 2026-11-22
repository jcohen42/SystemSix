#!/usr/bin/python
"""Functions for turning on the screen when an object is detected by an IR sensor."""

import logging
import subprocess
import time
import threading
import RPi.GPIO as IO
from settings import IS_WAYLAND, LOGGED_IN_USER


logger = logging.getLogger('app')


def detect_objects_internal():
    # Change these if your pins are plugged into different headers
    vcc_pin = 3
    out_pin = 8

    IO.setwarnings(False)
    IO.setmode(IO.BOARD)
    IO.setup(out_pin, IO.IN)
    IO.setup(vcc_pin, IO.OUT)

    lock = False
    while 1:
        if(IO.input(out_pin) == False):
            IO.output(vcc_pin, True)

            if(lock is False):
                logger.info("Obstacle detected. Turning on screen.")
                if(IS_WAYLAND):
                    subprocess.call(f"XAUTHORITY=~{LOGGED_IN_USER}/.Xauthority DISPLAY=:0 xset dpms force on && xset -dpms", shell=True)
                else:
                    subprocess.call("/usr/bin/wlr-randr --output HDMI-A-1 --on", shell=True)
                lock = True
                time.sleep(5)
        else:
            IO.output(vcc_pin, False)
            lock = False
        time.sleep(0.1)

def detect_objects():
    detector_thread = threading.Thread(target=detect_objects_internal, name="Object Detector")
    detector_thread.start()

def main():
    """Run program if called directly."""
    detect_objects_internal()
    

if __name__ == "__main__":
    main()
