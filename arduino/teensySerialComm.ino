//System Rover Sensors Block Ranging Code
//Author: Zach Caprai
//Date: 11/26/2017
//Description: Serial communication script from teensy to Raspberry pi for sonar.
#include <stdlib.h>

const int PWM_R = 12; // 9;
const int PWM_L = 14;

//const int StartStop_Pin = 7;
long PWM_PulseR;
long PWM_PulseL;
int R_mm;
int L_mm;
char buffer[5];

void setup()
{
    Serial1.begin(9600); //
}
void loop()
{
    //Set PWM_R = 12 to input to read in the pulse
    pinMode(PWM_R, INPUT);
    PWM_PulseR = pulseIn(PWM_R, HIGH);
    R_mm = PWM_PulseR / 1; //conversion from long to int.

    //Set PWM_L = 14 to input to read in the pulse
    pinMode(PWM_L, INPUT);
    PWM_PulseL = pulseIn(PWM_L, HIGH);
    L_mm = PWM_PulseL / 1;

    //Send Right sonar data with preceding 'R'
    Serial1.write('R');
    Serial1.flush();
    Serial1.print(itoa(R_mm, buffer, 10));
    Serial1.flush();

    delay(50); //small delay between communication

    //Send Left sonar data with preceding 'L'
    Serial1.write('L');
    Serial1.flush();
    Serial1.print(itoa(L_mm, buffer, 10));
    Serial1.flush();
}