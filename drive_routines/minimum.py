import dual_mc33926
import time
import servo
# (testing) add this script for startup
# sudo nano .bashrc

def forward():
    M_DRIVER = dual_mc33926.MotorDriver()
    M_DRIVER.set_speeds(480,1,384,1)
    M_DRIVER.enable()
    time.sleep(2)

    #slow down
    for speed in range(480,50,-1):
        time.sleep(0.03)
        M_DRIVER.set_speeds(speed,1,motor_cali(speed),1)

    M_DRIVER.disable()

#calibration constant for motors
def motor_cali(speed):
    return int(speed*(0.95))


if __name__ == "__main__":
    dual_mc33926.io_init_motor_drive()
    forward()
    #time.sleep(3)
    #servo.deploy_solar()
