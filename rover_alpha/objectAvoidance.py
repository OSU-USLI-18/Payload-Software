#!usr/bin/env python

import maxSonarTTY as Sonar
import dual_mc33926 as DualMc
from Enum import Enum
import time

# Sonar Constants
SONAR_THRESH = 1500

# Motor Constants
MOTOR_NORMAL_SP = 360
MOTOR_MAIN_TURN_SP = 240
MOTOR_OFF_TURN_SP = 120
TURN_TIME = 1

MOTOR_FWD = 1
MOTOR_BKWD = 0

def readSonar():
     LMeasure = []
     RMeasure = []
    for i in range(0,3):
        LMeasure.append(Sonar.measure(serialDevice, LeftSonarIndicator))
        RMeasure.append(Sonar.measure(serialDevice, RightSonarIndicator))

    LAvg = sum(LMeasure) / len(LMeasure)
    RAvg = sum(RMeasure) / len(RMeasure)

    return LAvg, RAvg
    

# Algorithm State
class State(Enum):
    FORWARD = 0
    AVOIDANCE = 1
    STALL = 2
    DEPLOY_SONAR = 3
    REVERSE = 4

# Initialization
motorDriver = DualMC.MotorDriver()

if __name__ == '__main__':
    
    State = State.FORWARD
    DualMC.io_init_motor_drive()
    LSonarVal = 0
    RSonarVal = 0

    while True:
        # Read Sonar Average
        LeftSonarVal, RightSonarVal = readSonar()

        if State == State.FORWARD:
            motorDriver.set_speeds(MOTOR_NORMAL_SP, MOTOR_FWD, MOTOR_NORMAL_SP, MOTOR_FWD)
            time.sleep(0.5)
            State = State.AVOIDANCE
    
        if State == State.AVOIDANCE:
            if LSonarVal < SONAR_THRESH:
                motorDriver.set_speeds(MOTOR_MAIN_TURN_SP, MOTOR_FWD, MOTOR_OFF_TURN_SP, MOTOR_FWD)
                time.sleep(TURN_TIME)
            elif RSonarVal < SONAR_THRESH:
                motorDriver.set_speeds(MOTOR_OFF_TURN_SP, MOTOR_FWD, MOTOR_MAIN_TURN_SP, MOTOR_FWD)
                time.sleep(TURN_TIME)
            State = State.FORWARD
