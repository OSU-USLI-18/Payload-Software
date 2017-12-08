/**************************************************************************
** Author: Kevin Turkington
** 12/7/17
** Description: Motor driver for raspberry PI using the wiringPi library.
** For Oregon State Universitys, USLI competition rover 
** http://osuusli.com/
** Based off of https://github.com/pololu/dual-mc33926-motor-driver-rpi
**************************************************************************/

#include <stdio.h>
#include <wiringPi.h>

using namespace std;

#ifndef DUAL_MC33926_RPI
#define DUAL_MC33926_RPI

const static int _maxSpeed = 480; // 19.2 MHz / 2 / 480 = 20 kHz

// NOTE: FORWARD = 0, BACKWARD = 1
enum motorDirection {FORWARD, BACKWARD};

bool ioInitialize();

class Motor
{
    private:
        int pwmPin;
        int directionPin;
        int enablePin;

        int speed;
        bool enabled;
        motorDirection direction;
    public:
        Motor(int,int,int);
        bool enable();
        bool disable();
        int setSpeed(int,motorDirection);

        motorDirection getDirection();
        int getSpeed();
        bool getEnabled();
};

class motorControl
{
    private:
        Motor *leftMotor;
        Motor *rightMotor;
    public:
        motorControl(int,int,int,int,int,int);

        void forward(int);
        void backward(int);
        void left(int,int);
        void right(int,int);
        void stop();
};

#endif



