#!/usr/bin/python3

from sonar  import Sonar

device = Sonar()
while True:
    print(device.measure())
