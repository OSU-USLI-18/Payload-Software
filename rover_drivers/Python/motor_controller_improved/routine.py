import dual_mc33926, time
# (testing) add this script for startup
# sudo nano .bashrc

def forward():
    M_DRIVER = dual_mc33926.MotorDriver()
    M_DRIVER.set_speeds(240,1,240,1)
    M_DRIVER.enable()
    time.sleep(15)
    M_DRIVER.disable()

def box():
    M_DRIVER = dual_mc33926.MotorDriver()
    M_DRIVER.set_speeds(240,1,240,1)
    M_DRIVER.enable()
    time.sleep(5)

    for i in range(1,3):
        M_DRIVER.set_speeds(240,0,240,1)
        time.sleep(2)

        M_DRIVER.set_speeds(240,1,240,1)
        time.sleep(5)
    
    M_DRIVER.disable()

if __name__ == "__name__":
    time.sleep(10)
    dual_mc33926.io_init_motor_drive()
    forward()





