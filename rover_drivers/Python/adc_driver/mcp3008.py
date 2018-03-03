# /usr/bin/env python
# https://github.com/adafruit/Adafruit_Python_MCP3008
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import time

AVGTHRESEHOLD = 3

#MCP specfic pins
CLK_pin  = 11
MISO_pin = 9
MOSI_pin = 10
CS_pin   = 8
mcp = Adafruit_MCP3008.MCP3008(clk=CLK_pin, cs=CS_pin, miso=MISO_pin, mosi=MOSI_pin)

def averageOutputs(ouputs):
    avg = 0
    for i in ouputs:
        avg += i
    return avg / len(ouputs)
        

if __name__ == "__main__":
    print('Reading MCP3008 values, press Ctrl-C to quit...')
    leftMic = []
    rightMic = []
    motorChnl = []

    while True:
        chn0 = mcp.read_adc(0)
        leftMic.append(chn0)

        chn1 = mcp.read_adc(1)
        rightMic.append(chn1)
        
        chn2 = mcp.read_adc(2)
        motorChnl.append(chn2)
        

        #chn3 = mcp.read_adc(3)
        #chn4 = mcp.read_adc(4)
        #chn5 = mcp.read_adc(5)
        #chn6 = mcp.read_adc(6)
        #chn7 = mcp.read_adc(7)
        if len(leftMic) > AVGTHRESEHOLD:
            print("LeftMic: {0}").format(averageOutputs(leftMic))
            leftMic = []

        if len(rightMic) > AVGTHRESEHOLD:
            print("RightMic: {0}").format(averageOutputs(rightMic))
            rightMic = []

        if len(motorChnl) > AVGTHRESEHOLD:
            print("Motor voltage: {0}").format(averageOutputs(motorChnl))
            motorChnl = []

        #print("{0},{1}").format(chn0, chn1)
        time.sleep(0.1)
