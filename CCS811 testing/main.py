"""Example usage basic driver CCS811.py"""

from machine import Pin, I2C
import time
import CCS811





def main():
    i2c = I2C(0)
    i2c = I2C(0, I2C.MASTER)
    i2c = I2C(0, pins=('P9', 'P10'))
    i2c.init(I2C.MASTER, baudrate=10000)
    # Adafruit sensor breakout has i2c addr: 90; Sparkfun: 91
    s = CCS811.CCS811(i2c=i2c)
    time.sleep(1)
    while True:
        if s.data_ready():
            print('eCO2: %d ppm, TVOC: %d ppb' % (s.eCO2, s.tVOC))
            time.sleep(1)

main()
