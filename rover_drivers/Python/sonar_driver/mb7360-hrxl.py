#############################################
# Kevin Turkington (Zainkai)                #
# 2/2/2018                                  #
# Sonar driver for MB7360 HRXL-MaxSonar-WR  #
#############################################
import wiringpi
import time

#https://tutorials-raspberrypi.com/raspberry-pi-ultrasonic-sensor-hc-sr04/
#https://www.raspberrypi.org/forums/viewtopic.php?f=33&t=32294

SONAR_CALIBRATION = 69 #actually find this calibration const.
SONAR_TIMEOUT = 3

def io_init_sonar(rd_pin,trig_pin):
    wiringpi.wiringPiSetupGpio()
    wiringpi.pinMode(trig_pin, wiringpi.GPIO.INPUT)
    wiringpi.pinMode(rd_pin, wiringpi.GPIO.OUTPUT)

class sonar_control(object):
    def __init__(self, rd_pin,trig_pin,timeout):
        self.rd_pin = rd_pin
        self.trig_pin = trig_pin
        self.timeout = timeout
    def get_range():
        # enable trigger.
        wiringpi.digitalWrite(self.trig_pin, 1)
        time.sleep(0.00001) # enough time to register write.
        wiringpi.digitalWrite(self.trig_pin, 0)

        start_time = time.time()
        time_delta = time.time() - start_time

        # only record time until read pin is high or time delta exceeds timeout.
        while wiringpi.digitalRead(self.rd_pin) != 1 or time_delta < self.timeout:
            time_delta = time.time() - start_time

        if time_delta > self.timeout:
            return -1

        return time_delta / SONAR_CALIBRATION #smallest unit of distance

    def get_range_cm():
        return self.get_range() / 324 # figure out const for getting range in (cm.)
    def get_range_m():
        return self.get_range() / 324 # figure out const for getting range in (m.)
    def get_range_in():
        return self.get_range() / 324 # figure out const for getting range in (in.)
    def get_range_ft():
        return self.get_range() / 324 # figure out const for getting range in (ft.)


if __name__ = "__main__":
    # write command line testing interface.
    # io_init_sonar(1,2)