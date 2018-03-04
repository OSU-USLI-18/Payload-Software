#!/usr/bin/python3

# sample script to read range values from Maxbotix ultrasonic rangefinder

from time import sleep
import maxSonarTTY

serialPort = "/dev/ttyAMA0"
maxRange = 5000  # change for 5m vs 10m sensor
sleepTime = 5
minMM = 9999
maxMM = 0

while True:
    mm = maxSonarTTY.measure(serialPort, "mm")
    if mm >= maxRange:
        print("no target")
        sleep(sleepTime)
        continue
    if mm < minMM:
        minMM = mm
    if mm > maxMM:
        maxMM = mm

    print("distance:", mm, "  min:", minMM, "max:", maxMM)
    sleep(sleepTime)
