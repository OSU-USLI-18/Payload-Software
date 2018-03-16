from sonar  import Sonar
from serial import Serial
from random import *
import threading

def dummy_serial():
    ser = Serial("COM9", 9600, timeout=5)
    sonars = ['L', 'R']
    while True:
        sonar = sonars[randint(0,1)]
        sample = randint(300, 330)
        to_write = (sonar + str(sample)).encode()
        ser.write(to_write)

def sonar_test():
    device = Sonar(device="COM10", timeout=5)
    while True:
        print(device.measure())

output = threading.Thread(target=dummy_serial)
input = threading.Thread(target=sonar_test)

output.start()
input.start()
