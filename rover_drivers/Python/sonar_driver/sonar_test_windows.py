#!/usr/bin/python3

from sonar  import Sonar
from serial import Serial
from random import *
import threading

def dummy_serial():
    ser = Serial("COM9", 9600, timeout=3)
    sonars = ['L', 'R']
    while True:
        sonar = sonars[randint(0,1)]
        sample = randint(299, 5000)
        to_write = (sonar + str(sample)).encode()
        ser.write(to_write)

def sonar_test():
    indicators = {b'L': "Left Sonar", b'R': "Right Sonar"}
    device = Sonar(device="COM10")
    while True:
        device.pretty_measure()

output = threading.Thread(target=dummy_serial)
input = threading.Thread(target=sonar_test)

output.start()
input.start()
