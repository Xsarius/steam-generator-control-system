import digitalio, adafruit_max31865, board

class Pt100_SPI():
    def __init__(self, pinNum, wires=4):
        self.pin = pinNum
        self.spi = board.SPI()
        self.cs = digitalio.DigitalInOut(self.pin)
        self.sensor = adafruit_max31865.MAX31865(self.spi, self.cs, wires=wires)

    def getTemp(self):
        return f'%.2f' % self.sensor.temperature