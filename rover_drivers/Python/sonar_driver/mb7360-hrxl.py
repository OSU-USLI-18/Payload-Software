import wiringpi
import time
from enum import Enum

#https://tutorials-raspberrypi.com/raspberry-pi-ultrasonic-sensor-hc-sr04/
#https://www.raspberrypi.org/forums/viewtopic.php?f=33&t=32294

class sonar_control(object):
    def __init__(self, pwm_pin):
        self.pwm_pin = pwm_pin
        wiringpi.pinMode(pwm_pin,wiringpi.GPIO.OUTPUT)

    def get_range():
        #pulseIn replica
