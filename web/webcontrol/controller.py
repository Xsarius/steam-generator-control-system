from web.settings import DEBUG, PINS, KELLER_CONFIG
from webcontrol.sensors import devices, pressure_sensors, temp_sensors
from collections import defaultdict
import RPi.GPIO as gpio
import timeloop, time
from webcontrol.models import SteamGenerator

# Periodic task handlers
t1 = timeloop.Timeloop()
t2 = timeloop.Timeloop()
t1.start()
t2.start()
curr_id = 0

class SGController:
    def __init__(self):
        print("SGcontroller setup started.")
        failed_to_connect = {}
        self.control_commands = defaultdict(int)
        gpio.setmode(gpio.BCM)
        self.data_save_started = False

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
            self.heater_w1 = devices.Heater_SSR(pinNum=PINS['HEATER_1'], maxpower=2667)
            failed_to_connect["Heater: water (1)"] = "connected"
        except:
            failed_to_connect["Heater: water (1)"] = "failed"
        try:
            self.heater_w2 = devices.Heater_SSR(pinNum=PINS['HEATER_2'], maxpower=2667)
            failed_to_connect["Heater: water (2)"] = "connected"
        except:
            failed_to_connect["Heater: water (2)"] = "failed"
        try:
            self.heater_w3 = devices.Heater_SSR(pinNum=PINS['HEATER_3'], maxpower=2667)
            failed_to_connect["Heater: water (3)"] = "connected"
        except:
            failed_to_connect["Heater: water (3)"] = "failed"
        try:
            self.heater_s1 = devices.Heater_SSR(pinNum=PINS['HEATER_STEAM_1'], maxpower=954)
            failed_to_connect["Heater: steam"] = "connected"
        except:
            failed_to_connect["Heater: steam"] = "failed"

        print("SG controller setup finished.")
        print("Result:")
        print(failed_to_connect)

    def set_commands(self, commands):
        commands_changed = 0

        if(DEBUG):
            print("self commands set")

        if(self.control_commands['heater_1_power'] != commands['heater_1_power']):
            self.control_commands['heater_1_power'] = commands['heater_1_power']
            commands_changed += 1

        if(self.control_commands['heater_2_power'] != commands['heater_2_power']):
            self.control_commands['heater_2_power'] = commands['heater_2_power']
            commands_changed += 1

        if(self.control_commands['heater_3_power'] != commands['heater_3_power']):
            self.control_commands['heater_3_power'] = commands['heater_3_power']
            commands_changed += 1

        if(self.control_commands['heater_st_power'] != commands['heater_steam_power']):
            self.control_commands['heater_st_power'] = commands['heater_steam_power']
            commands_changed += 1

        if(self.control_commands['valve'] != commands['valve']):
            self.control_commands['valve'] = commands['valve']
            commands_changed += 1

        if(DEBUG):
            print(commands_changed)

        return commands_changed

    def get_output(self):
        if(DEBUG):
            print("controller output")

        if(DEBUG):
            output = {
                'water_temp': self.temp_sensor_w1.getTemp(),
                'steam_temp_1': self.temp_sensor_s1.getTemp(),
                'steam_temp_2': self.temp_sensor_s2.getTemp(),
                'heater_1': self.heater_w1.state(),
                'heater_2': self.heater_w2.state(),
                'heater_3': self.heater_w3.state(),
                'heater_st': self.heater_s1.state(),
                'valve': self.valve.state(),
                'save': int(self.data_save_started)
            }

        if(not DEBUG):
            output = {
                'water_temp': self.temp_sensor_w1.getTemp(),
                'steam_temp_1': self.temp_sensor_s1.getTemp(),
                'steam_temp_2': self.temp_sensor_s2.getTemp(),
                'pressure': self.pressure_sensor.read('pressure'),
                'ps_temp': self.pressure_sensor.read('temp'),
                'heater_1': self.heater_w1.state(),
                'heater_2': self.heater_w2.state(),
                'heater_3': self.heater_w3.state(),
                'heater_st': self.heater_s1.state(),
                'valve': self.valve.state(),
                'save': int(self.data_save_started)
            }

        return output

    def control_loop(self):
        if(DEBUG):
            print("control loop entered\n")

        if(self.control_commands['heater_st_power']):
            self.heater_s1.on()
        else:
            self.heater_s1.off()

        if(self.control_commands['heater_1_power']):
            self.heater_w1.on()
        else:
            self.heater_w1.off()

        if(self.control_commands['heater_2_power']):
            self.heater_w2.on()
        else:
            self.heater_w2.off()

        if(self.control_commands['heater_3_power']):
            self.heater_w3.on()
        else:
            self.heater_w3.off()

        if(self.control_commands['valve']):
            self.valve.open()
        else:
            self.valve.close()

    def soft_shutdown(self):
        self.heater_w1.off()
        self.heater_w2.off()
        self.heater_w3.off()
        self.heater_s1.off()

    def start_data_save(self):
        curr_id = SteamGenerator.objects.latest('measurement_num') + 1
        self.data_save_started = True

    def stop_data_save(self):
        self.data_save_started = False

    def emergency_shutdown(self):
        if(DEBUG):
            print("Emergency stop")
        pass

    def soft_shutdown(self):
        if(DEBUG):
            print("Soft stop")
        pass

    def get_data_from_db(self):
        curr_id = SteamGenerator.objects.latest('measurement_num')
        data = SteamGenerator.objects.filter(measurement_num=curr_id).all()
        return data