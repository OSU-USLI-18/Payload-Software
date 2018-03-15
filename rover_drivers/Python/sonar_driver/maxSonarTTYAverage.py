#!/usr/bin/python3

from time   import time
from serial import Serial

ser_device  = "/dev/ttyAMA0"   # default for RaspberryPi
max_wait    = 5                # seconds to try for a good reading before quitting
l_indicator = b'L'
r_indicator = b'R'

def measure(ser_device, l_char, r_char):
    start_time  = time()
    count       = 0
    l_buffer    = []
    r_buffer    = []

    while time() < start_time + max_wait:
        if ser.inWaiting():
            bytes_to_read = ser.inWaiting()
            test_data = ser.read(bytes_to_read)
            if test_data.startswith(l_char):
                start_char = l_char
            elif test_data.startswith(r_char):
                start_char = r_char
            else:
                continue
            try:
                sensor_data = test_data.lstrip(charSrt).decode("utf-8")
            except UnicodeDecodeError:
                continue
            try:
                mm = int(sensorData)
            except ValueError:
                continue
            if mm > 4500:
                continue
            data_buffer[count] = mm
            
            if count == 2:
                avg = sum(data_buffer) / 3.0
                for x in data_buffer:
                    if abs(x - avg) > (0.2 * avg):
                        data_buffer.remove(x)
                if len(data_buffer) > 0:
                    result = sum(data_buffer) / float(len(data_buffer))
                    return (result
                else:
                    return None
                    
            count += 1

    ser.close()
    raise RuntimeError("Expected serial data not received")

def sonarUnitConvert(val_mm, unit):
    if unit == None:
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

if __name__ == '__main__':
    ser = Serial(serialDevice, 9600, 8, 'N', 1, timeout=1)
    while True:
        print(measure(ser, l_indicator, r_indicator)

        Rmeasurement = measure(ser, r_indicator)
        if Rmeasurement < 4500:
            print("Right distance = ", Rmeasurement)
