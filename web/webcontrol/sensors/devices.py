import RPi.GPIO as GPIO

class Heater_SSR():
    def __init__(self, pinNum, maxpower = 0, power=0):
        self.pin = pinNum
        self.power = power
        self.maxpower = maxpower
        GPIO.setup(pinNum, GPIO.OUT)

    def state(self):
        if(self.power > 0):
            return 1
        return 0

    def on(self):
        GPIO.output(self.pin, GPIO.HIGH)
        self.power=self.maxpower

    def off(self):
        GPIO.output(self.pin, GPIO.LOW)
        self.power=0

class Valve_SRR():
    def __init__(self, pinNum, state=0):
        self.pin = pinNum
        self.curr_state = state
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.remove_event_detect(self.pin)

    def open(self):
        GPIO.output(self.pin, GPIO.HIGH)
        self.curr_state = 1

    def close(self):
        GPIO.output(self.pin, GPIO.LOW)
        self.curr_state = 0

    def state(self):
        return self.curr_state