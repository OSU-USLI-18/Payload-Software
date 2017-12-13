#include "dual_mc33926_rpi.hpp"

Motor::Motor(int pulsewmPin,int dirPin, int enPin){
    pwmPin = pulsewmPin;
    directionPin = dirPin;
    enablePin = enPin;

    speed = 0;
    enabled = false;
    direction = FORWARD;

    //need eces to describe what some of this does.
    pinMode(pwmPin, PWM_OUTPUT);
    pwmSetMode(PWM_MODE_MS);
    pwmSetRange(_maxSpeed);
    pwmSetClock(2);

    pinMode(directionPin,OUTPUT);
    pinMode(enablePin,OUTPUT);
}

bool Motor::enable(){
    digitalWrite(enablePin, 1);
    enabled = true;

    return enabled;
}

bool Motor::disable(){
    digitalWrite(enablePin, 0);
    enabled = false;

    return enabled;
}

int Motor::setSpeed(int newSpeed, motorDirection newdir){
    direction = newdir;

    if(-newSpeed > _maxSpeed || newSpeed > _maxSpeed){
        speed = _maxSpeed;
    }
    else if(newSpeed < 0){
        speed = -newSpeed;
    }
    else{
        speed = newSpeed;
    }

    digitalWrite(directionPin, direction);
    pwmWrite(pwmPin, speed);

    return speed;
}

motorDirection Motor::getDirection(){
    return direction;
}

int Motor::getSpeed(){
    return speed;
}

bool Motor::getEnabled(){
    return enabled;
}

//make inputs an interfact later.
motorControl::motorControl(
    int pulsewmPinLeft, int dirPinLeft, int enPinLeft,
    int pulsewmPinRight, int dirPinRight, int enPinRight
){
    leftMotor = new Motor(pulsewmPinLeft,dirPinLeft,enPinLeft);
    rightMotor = new Motor(pulsewmPinRight,dirPinRight,enPinRight);
}

void motorControl::forward(int speed){
    leftMotor->disable();
    rightMotor->disable();

    leftMotor->setSpeed(speed,FORWARD);
    rightMotor->setSpeed(speed,FORWARD);

    leftMotor->enable();
    rightMotor->enable();
}

void motorControl::backward(int speed){
    leftMotor->disable();
    rightMotor->disable();

    leftMotor->setSpeed(speed,BACKWARD);
    rightMotor->setSpeed(speed,BACKWARD);

    leftMotor->enable();
    rightMotor->enable();
}

void motorControl::left(int speedL,int speedR){
    leftMotor->disable();
    rightMotor->disable();

    leftMotor->setSpeed(speedL,BACKWARD);
    rightMotor->setSpeed(speedR,FORWARD);

    leftMotor->enable();
    rightMotor->enable();
}

void motorControl::right(int speedL,int speedR){
    leftMotor->disable();
    rightMotor->disable();

    leftMotor->setSpeed(speedL,FORWARD);
    rightMotor->setSpeed(speedR,BACKWARD);

    leftMotor->enable();
    rightMotor->enable();
}

void motorControl::stop(){
    leftMotor->disable();
    rightMotor->disable();

    leftMotor->setSpeed(0,FORWARD);
    rightMotor->setSpeed(0,FORWARD);
}

int main(int argc, char** argv)
{
    if(wiringPiSetupGpio() == -1){
        printf("someting went wrong!\n");
        return 1;
    }
    
    printf("wiringPi is working!\n");

    motorControl *driver = new motorControl(12,24,22,13,25,23);
    driver->stop();

    printf("ran some functions\n");

    return 0;
}