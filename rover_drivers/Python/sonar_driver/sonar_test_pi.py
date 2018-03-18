#!/usr/bin/python3

from sonar import Sonar

device = Sonar(threshold=0.1, buffer_size=5)
while True:
    device.pretty_measure()
