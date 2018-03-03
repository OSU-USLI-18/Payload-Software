#!/usr/bin/python3

from time   import time
from serial import Serial

serialDevice = "/dev/ttyAMA0"   # default for RaspberryPi
maxwait      = 3                # seconds to try for a good reading before quitting

def measure(portName, unit):
    ser         = Serial(portName, 9600, 8, 'N', 1, timeout=1)
    timeStart   = time()
    valueCount  = 0

    while time() < timeStart + maxwait:
        if ser.inWaiting():
            bytes_to_read = ser.inWaiting()
            valueCount += 1
            if valueCount < 2: # 1st reading may be partial number; throw it out
                continue
            testData = ser.read(bytes_to_read)
            if not testData.startswith(b'R'):
                # data received did not start with R
                continue
            try:
                sensorData = testData.decode('utf-8').lstrip('R')
            except UnicodeDecodeError:
                # data received could not be decoded properly
                continue
            try:
                mm = int(sensorData)
            except ValueError:
                # value is not a number
                continue
            ser.close()

            if not isInstance(unit, str):
                return mm
            elif unit.lower() in ["cm", "centimeter", "centimeters"]:
                return (mm * 10)
            elif unit.lower() in ["m", "meter", "meters"]:
                return (mm * 1000)
            elif unit.lower() in ["in", "in.", "inch", "inches"]:
                return (mm * 25.4)
            elif unit.lower() in ["ft", "ft.", "foot", "feet"]:
                return (mm * 304.8)
            else:
                return mm

    ser.close()
    raise RuntimeError("Expected serial data not received")

if __name__ == '__main__':
    measurement = measure(serialDevice, "mm")
    print("distance = ", measurement)
