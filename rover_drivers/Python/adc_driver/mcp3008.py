# https://github.com/adafruit/Adafruit_Python_MCP3008
# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import time

#MCP specfic pins
CLK_pin  = 11
MISO_pin = 9
MOSI_pin = 10
CS_pin   = 8
mcp = Adafruit_MCP3008.MCP3008(clk=CLK_pin, cs=CS_pin, miso=MISO_pin, mosi=MOSI_pin)

# zachs specficed pins
mic1_pin = 22
mic2_pin = 23

if __name__ == "__main__":
    print('Reading MCP3008 values, press Ctrl-C to quit...')
    while True:
        chn1 = mcp.read_adc(mic1_pin)
        chn2 = mcp.read_adc(mic2_pin)
        print("mic 1 values: {0}").format(chn1)
        print("mic 2 values: {0}").format(chn2)
        time.sleep(0.5)

    


