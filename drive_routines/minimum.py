import dual_mc33926, time, servo
# (testing) add this script for startup
# sudo nano .bashrc

def forward():
    M_DRIVER = dual_mc33926.MotorDriver()
    M_DRIVER.set_speeds(480,1,480,1)
    M_DRIVER.enable()
    time.sleep(10)
    M_DRIVER.disable()

if __name__ == "__main__":
    dual_mc33926.io_init_motor_drive()
    forward()
    time.sleep(5)
    servo.deploy_solar()



