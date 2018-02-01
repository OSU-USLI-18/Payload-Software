#!/usr/bin/env python2 
import wiringpi
import time
import sys

#move to a constants file.
MAX_SPEED = 480  # 19.2 MHz / 2 / 480 = 20 kHz
io_initialized = False

def io_init():
    global io_initialized
    if io_initialized:
        return

    wiringpi.wiringPiSetupGpio()
    wiringpi.pinMode(12, wiringpi.GPIO.PWM_OUTPUT)
    wiringpi.pinMode(13, wiringpi.GPIO.PWM_OUTPUT)

    wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)
    wiringpi.pwmSetRange(MAX_SPEED)
    wiringpi.pwmSetClock(2)

    wiringpi.pinMode(22, wiringpi.GPIO.OUTPUT)
    wiringpi.pinMode(23, wiringpi.GPIO.OUTPUT)
    wiringpi.pinMode(24, wiringpi.GPIO.OUTPUT)
    wiringpi.pinMode(25, wiringpi.GPIO.OUTPUT)

    io_initialized = True

class Motor(object):
    def __init__(self, pwm_pin, direction_pin, enable_pin):
        self.pwm_pin = pwm_pin
        self.direction_pin = direction_pin
        self.enable_pin = enable_pin

    def enable(self):
        io_init()
        wiringpi.digitalWrite(self.enable_pin, 1)

    def disable(self):
        io_init()
        wiringpi.digitalWrite(self.enable_pin, 0)

    def setSpeed(self, new_speed, motorDirection):
        if new_speed > MAX_SPEED:
            new_speed = MAX_SPEED
        elif new_speed < 0:
            new_speed = -new_speed

        wiringpi.digitalWrite(self.direction_pin, motorDirection)
        wiringpi.pwmWrite(self.pwm_pin, new_speed)




#note: for direction values use Direction class.
class motorDrive(object):
    def __init__(self):
        self.motor1 = Motor(12, 24, 22)
        self.motor2 = Motor(13, 25, 23)
    def enable(self):
        self.motor1.enable()
        self.motor2.enable()
    def disable(self):
        self.motor1.disable()
        self.motor2.disable()
    def setSpeeds(self, m1_speed, m1_dir, m2_speed, m2_dir):
        self.motor1.setSpeed(m1_speed,m1_dir)
        self.motor2.setSpeed(m2_speed,m2_dir)


if __name__ == "__main__":
    mDrive = motorDrive()
    io_init()

    if "-h" in sys.argv or "-help" in sys.argv:
        print("Help text for pololu dual_mc33926.")
        print("-h, -help : for help text.")
        print("-e, -enable : to enable both motors.")
        print("-d, -disable : to disable both motors.")
        print("-ss, -setspeed : to setup both motors")
        print("\tUsage:\n\t-ss <motor1 pwm> <motor1 dir> <motor2 pwm> <motor2 dir>")
        print("\tpwm range: 0 - 480\n\tdirections: 0 - forward, 1 - backward")
    elif "-e" in sys.argv or "-enable" in sys.argv:
        print("Enabling Motors...")
        mDrive.enable()
    elif "-d" in sys.argv or "-disable" in sys.argv:
        print("Disabling Motors...")
        mDrive.disable()
    elif ("-ss" in sys.argv or "-setspeed" in sys.argv) and len(sys.argv) == 6:
        trunArg = sys.argv[2:]
        print("setting motor1 to pwm: {0}").format(int(trunArg[0]))
        print("setting motor1 to direction: {0}").format(int(trunArg[1]))
        print("setting motor2 to pwm: {0}").format(int(trunArg[2]))
        print("setting motor2 to direction: {0}").format(int(trunArg[3]))
        mDrive.setSpeeds( (int(trunArg[0])) , (int(trunArg[1])) , (int(trunArg[2])) , (int(trunArg[3])) )
    else:
        print("Invalid command arguments.")
        print("-h, -help : for help text.")
