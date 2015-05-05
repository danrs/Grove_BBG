from Adafruit_I2C import Adafruit_I2C
import time

getData = int()
analogVal = int()

i2c = Adafruit_I2C(0x55)        
i2c.write8(0x02, 0x20)

class I2C_ADC():
    def __init__(self):
        self.ADDR_ADC121 = 0x55
        self.V_REF = 3.00
        self.REG_ADDR_RESULT = 0x00
        self.REG_ADDR_ALERT = 0x01
        self.REG_ADDR_CONFIG = 0x02
        self.REG_ADDR_LIMITL = 0x03
        self.REG_ADDR_LIMITH = 0x04
        self.REG_ADDR_HYST = 0x05
        self.REG_ADDR_CONVL = 0x06
        self.REG_ADDR_CONVH = 0x07
        
    def read_adc(self):
        data = 0x0000
        data = i2c.readU16(self.REG_ADDR_RESULT)
        time.sleep(0.1)
        return data
        
if __name__=="__main__":
    while True:
	adc = I2C_ADC()
	print 'sensor value ', float(adc.read_adc() / 655.35), '%'
        time.sleep(1)        
