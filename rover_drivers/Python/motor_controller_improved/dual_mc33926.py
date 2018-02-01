import wiringpi
import time
from enum import Enum

class Direction(Enum):
    Forward = 0
    Backward = 1

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
        wiringpi.digitalWrite(self.enable_pin, 0)

    def disable(self):
        io_init()
        wiringpi.digitalWrite(self.enable_pin, 1)

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
    print("verifying motor drivers work correctly.")
    motorDriver = motorDrive()
    motorDriver.enable()

    while True:
        time.sleep(5)
        print("running motors...")
        motorDriver.setSpeeds(480,0,480,0)
