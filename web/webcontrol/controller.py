from web.settings import DEBUG, PINS, KELLER_CONFIG
from webcontrol.sensors import devices, pressure_sensors, temp_sensors
from collections import defaultdict
import RPi.GPIO as gpio
import timeloop, time
from webcontrol.models import SteamGenerator

# Periodic task handlers
t1 = timeloop.Timeloop()

t1.start()

curr_id = 0

class SGController:
    def __init__(self, P_coeff = 1, I_coeff = 1, D_coeff = 0):
        self.control_params = defaultdict(int)
        gpio.setmode(gpio.BCM)
        self.data_save_started = False
        self.pid_coeffs = {
            'P': P_coeff,
            'I': I_coeff,
            'D': D_coeff,
        }

        try:
            self.temp_sensor_w1 = temp_sensors.Pt100_SPI(pinNum=PINS['TEMP_WATER_1'])
        except:
            print("Water temperature sensor no.1 failed to connet")
        try:
            self.temp_sensor_s1 = temp_sensors.Pt100_SPI(pinNum=PINS['TEMP_STEAM_1'])
        except:
            print("Steam temperature sensor no.2 failed to connet")
        try:
            self.temp_sensor_s2 = temp_sensors.Pt100_SPI(pinNum=PINS['TEMP_STEAM_2'])
        except:
            print("Steam temperature sensor no.2 failed to connet")
        try:
            self.pressure_sensor = pressure_sensors.Keller23sx(
                registers_dict=KELLER_CONFIG['registers'],
                port=KELLER_CONFIG['port'],
                unit=KELLER_CONFIG['unit'])
        except:
            print("Pressure sensor no.1 failed to connet")
        try:
            self.valve = devices.Valve_SRR(pinNum=PINS['VALVE_1'])
        except:
            print("Valve failed to connet")
        try:
            self.heater_w1 = devices.Heater_SSR(pinNum=PINS['HEATER_1'], maxpower=2667)
        except:
            print("Water heater no.1 failed to connet")
        try:
            self.heater_w2 = devices.Heater_SSR(pinNum=PINS['HEATER_2'], maxpower=2667)
        except:
            print("Water heater no.2 failed to connet")
        try:
            self.heater_w3 = devices.Heater_SSR(pinNum=PINS['HEATER_3'], maxpower=2667)
        except:
            print("Water heater no.3 failed to connet")
        try:
            self.heater_s1 = devices.Heater_SSR(pinNum=PINS['HEATER_STEAM_1'], maxpower=954)
        except:
            print("Steam heater no.1 failed to connet")

    def get_output(self):
        if(DEBUG):
            print("controller output")

        output = {
            'water_temp': self.temp_sensor_w1.getTemp(),
            'steam_temp_1': self.temp_sensor_s1.getTemp(),
            'steam_temp_2': self.temp_sensor_s2.getTemp(),
            'heater_w1': self.heater_w1.state(),
            'heater_w2': self.heater_w2.state(),
            'heater_w3': self.heater_w3.state(),
            'heater_st': self.heater_s1.state(),
            'valve': self.valve.state(),
            'save': int(self.data_save_started)
        }

        if(not DEBUG):
            output['pressure'] = self.pressure_sensor.read('pressure')
            output['pid_signal'] = 0
            # output['voltage_ph1'] = self.power_meter_ph1.read('voltage')
            # output['current_ph1'] = self.power_meter_ph1.read('current')
            # output['active_power_ph1'] = self.power_meter_ph1.read('active_power')
            # output['voltage_ph2'] = self.power_meter_ph2.read('voltage')
            # output['current_ph2'] = self.power_meter_ph2.read('current')
            # output['active_power_ph2'] = self.power_meter_ph2.read('active_power')
            # output['voltage_ph3'] = self.power_meter_ph3.read('voltage')
            # output['current_ph3'] = self.power_meter_ph3.read('current')
            # output['active_power_ph3'] = self.power_meter_ph3.read('active_power')

        return output

    def control_loop(self):
        if(DEBUG):
            print("Control loop\n")

        if(self.control_params['heater_st']):
            self.heater_s1.on()
        else:
            self.heater_s1.off()

        if(self.control_params['heater_w1']):
            self.heater_w1.on()
        else:
            self.heater_w1.off()

        if(self.control_params['heater_w2']):
            self.heater_w2.on()
        else:
            self.heater_w2.off()

        if(self.control_params['heater_w3']):
            self.heater_w3.on()
        else:
            self.heater_w3.off()

        if(self.control_params['valve']):
            self.valve.open()
        else:
            self.valve.close()

    def soft_shutdown(self):
        self.heater_w1.off()
        self.heater_w2.off()
        self.heater_w3.off()
        self.heater_s1.off()
        self.valve.close()

    def start_data_save(self):
        curr_id = SteamGenerator.objects.latest('measurement_num') + 1
        self.data_save_started = True

    def stop_data_save(self):
        self.data_save_started = False

    def emergency_shutdown(self):
        if(DEBUG):
            print("Emergency stop")
        pass

    def get_data_from_db(self):
        curr_id = SteamGenerator.objects.latest('measurement_num')
        data = SteamGenerator.objects.filter(measurement_num=curr_id).all()
        return data