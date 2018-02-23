# https://github.com/adafruit/Adafruit_Python_MCP3008
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import time

#MCP specfic pins
CLK_pin  = 23
MISO_pin = 21
MOSI_pin = 19
CS_pin   = 24
mcp = Adafruit_MCP3008.MCP3008(clk=CLK_pin, cs=CS_pin, miso=MISO_pin, mosi=MOSI_pin)

if __name__ == "__main__":
    print('Reading MCP3008 values, press Ctrl-C to quit...')
    while True:
        chn0 = mcp.read_adc(0)
        chn1 = mcp.read_adc(1)
        #chn2 = mcp.read_adc(2)
        #chn3 = mcp.read_adc(3)
        #chn4 = mcp.read_adc(4)
        #chn5 = mcp.read_adc(5)
        #chn6 = mcp.read_adc(6)
        #chn7 = mcp.read_adc(7)
        print("{0},{1}").format(chn0, chn1)
        time.sleep(0.5)

    


