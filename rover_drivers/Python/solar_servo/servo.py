import time
import RPi.GPIO as GPIO


def deploy_solar():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(12,GPIO.OUT)

    pwm = GPIO.PWM(12,50)
    pwm.start(0)

    for i in range(0,50):
        pwm.ChangeDutyCycle(5)
        time.sleep(0.1)
        pwm.ChangeDutyCycle(0)
        time.sleep(0.1)

    pwm.stop()
    GPIO.cleanup()
