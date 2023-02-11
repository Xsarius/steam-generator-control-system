from web.settings import DEBUG, PINS, KELLER_CONFIG, LUMEL_CONFIG
from webcontrol.sensors import devices, pressure_sensors, temp_sensors, power_meters
from collections import defaultdict
import RPi.GPIO as gpio, simple_pid, os
from webcontrol.models import SteamGenerator

class SGController:
    def __init__(self):
        print("SGcontroller setup started.")
        failed_to_connect = {}
        gpio.setmode(gpio.BCM)

        self.control_params = defaultdict(int)
        self.data_save_started = False
        self.pid = simple_pid.PID(Kp=os.environ.get("P_COEF"),Ki=os.environ.get("I_COEF"), Kd=os.environ.get("D_COEF"))
        self.curr_measurement_id = 0
        self.output = defaultdict(int)

        try:
            self.temp_sensor_w1 = temp_sensors.Pt100_SPI(pinNum=PINS['TEMP_WATER_1'])
            failed_to_connect["Temp sensor: water"] = "connected"
        except:
            failed_to_connect["Temp sensor: water"] = "failed"
        try:
            self.temp_sensor_s1 = temp_sensors.Pt100_SPI(pinNum=PINS['TEMP_STEAM_1'])
            failed_to_connect["Temp sensor: steam (1)"] = "connected"
        except:
            failed_to_connect["Temp sensor: steam (1)"] = "failed"
        try:
            self.temp_sensor_s2 = temp_sensors.Pt100_SPI(pinNum=PINS['TEMP_STEAM_2'])
            failed_to_connect["Temp sensor: steam (2)"] = "connected"
        except:
            failed_to_connect["Temp sensor: steam (2)"] = "failed"
        try:
            self.pressure_sensor = pressure_sensors.Keller23sx(
                registers_dict=KELLER_CONFIG['registers'],
                port=KELLER_CONFIG['port'],
                unit=KELLER_CONFIG['unit'])
            failed_to_connect["Pressure sensor"] = "connected"
        except:
            failed_to_connect["Pressure sensor"] = "failed"
        try:
            self.valve = devices.Valve_SRR(pinNum=PINS['VALVE_1'])
            failed_to_connect["Valve"] = "connected"
        except:
            failed_to_connect["Valve"] = "failed"
        try:
            self.heater_w1 = devices.Heater_SSR(pinNum=PINS['HEATER_1'])
            failed_to_connect["Heater: water (1)"] = "connected"
        except:
            failed_to_connect["Heater: water (1)"] = "failed"
        try:
            self.heater_w2 = devices.Heater_SSR(pinNum=PINS['HEATER_2'])
            failed_to_connect["Heater: water (2)"] = "connected"
        except:
            failed_to_connect["Heater: water (2)"] = "failed"
        try:
            self.heater_w3 = devices.Heater_SSR(pinNum=PINS['HEATER_3'])
            failed_to_connect["Heater: water (3)"] = "connected"
        except:
            failed_to_connect["Heater: water (3)"] = "failed"
        try:
            self.heater_s1 = devices.Heater_SSR(pinNum=PINS['HEATER_STEAM_1'])
            failed_to_connect["Heater: steam"] = "connected"
        except:
            failed_to_connect["Heater: steam"] = "failed"
        try:
            self.stop_pin = devices.Heater_SSR(pinNum=PINS['STOP'])
            failed_to_connect["Stop pin"] = "active"
            self.stop_pin.on()
        except:
            failed_to_connect["Stop pin"] = "inactive"
        try:
            self.power_meter = power_meters.LUMEL_N27P(unit=LUMEL_CONFIG['unit'])
            failed_to_connect["Power meter 1"] = "connected"
        except:
            failed_to_connect["Power meter 1"] = "failed"

        print("SG controller setup finished.")
        print("Result:")
        print(failed_to_connect)

    def control_loop(self):
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

        if(self.control_params['power']):
            self.stop_pin.on()
        else:
            self.stop_pin.off()

    def start_data_save(self):
        try:
            curr_id = SteamGenerator.objects.latest('measurement_num') + 1
        except:
            curr_id = 1
        print("Save to db started.\n")
        self.data_save_started = True

    def stop_data_save(self):
        print("Save to db stopped.\n")
        self.data_save_started = False

    def emergency_shutdown(self):
        self.stop_pin.off()

    def soft_shutdown(self):
        self.heater_w1.off()
        self.heater_w2.off()
        self.heater_w3.off()
        self.heater_s1.off()
        self.valve.close()

    def get_data_from_db(self):
        try:
            self.curr_measurement_id = SteamGenerator.objects.latest('measurement_num')
        except:
            self.curr_measurement_id = 1

        try:
            data = SteamGenerator.objects.filter(measurement_num=self.curr_measurement_id).all()
        except:
            raise()

        return data