from web.settings import MAX_TEMP, MAX_PRESSURE, BACKUP_FILE
import datetime, timeloop
from .controller import SGController
from .models import SteamGenerator
from pyXSteam.XSteam import XSteam

controller = SGController()
steamTable = XSteam(XSteam.UNIT_SYSTEM_MKS)

# Periodic task handlers
t1 = timeloop.Timeloop()
t2 = timeloop.Timeloop()

@t1.job(interval=datetime.timedelta(milliseconds=200))
def set_output():
    controller.output['water_temp'] = int(controller.temp_sensor_w1.getTemp()),
    controller.output['steam_temp_1'] = int(controller.temp_sensor_s1.getTemp()),
    controller.output['steam_temp_2'] = int(controller.temp_sensor_s2.getTemp()),
    controller.output['heater_w1'] = int(controller.heater_w1.state()),
    controller.output['heater_w2'] = int(controller.heater_w2.state()),
    controller.output['heater_w3'] = int(controller.heater_w3.state()),
    controller.output['heater_st'] = int(controller.heater_s1.state()),
    controller.output['valve'] = int(controller.valve.state()),
    controller.output['save'] = int(controller.data_save_started),
    controller.output['pid_signal'] = int(0),

    with open(BACKUP_FILE, "a") as backup_file:
        for key, value in controller.output.items():
            backup_file.write('%s:%s' % (key, value))

        backup_file.write('\n')

# @t1.job(interval=datetime.timedelta(seconds=1))
# def get_modbus_readouts():
#         controller.output['pressure'] = int(controller.pressure_sensor.read('pressure')),
#         controller.output['voltage_ph1'] = int(controller.power_meter.read('voltage_ph1')),
#         controller.output['current_ph1'] = int(controller.power_meter.read('current_ph1')),
#         controller.output['active_power_ph1'] = int(controller.power_meter.read('active_power_ph1')),
#         controller.output['voltage_ph2'] = int(controller.power_meter.read('voltage_ph2')),
#         controller.output['current_ph2'] = int(controller.power_meter.read('current_ph2')),
#         controller.output['active_power_ph2'] = int(controller.power_meter.read('active_power_ph2')),
#         controller.output['voltage_ph3'] = int(controller.power_meter.read('voltage_ph3')),
#         controller.output['current_ph3'] = int(controller.power_meter.read('current_ph3')),
#         controller.output['active_power_ph3'] = int(controller.power_meter.read('active_power_ph3')),

@t1.job(interval=datetime.timedelta(seconds=1))
def watchdog():
    if(controller.output['water_temp'] >= MAX_TEMP or
        controller.output['steam_temp_1'] >= MAX_TEMP or
        controller.output['steam_temp_2'] >= MAX_TEMP or
        controller.output['pressure'] >= MAX_PRESSURE):

        controller.soft_shutdown()

@t1.job(interval=datetime.timedelta(milliseconds=200))
def pid_loop():
    curr_temp = int(controller.output['steam_temp_1'])
    curr_press = int(controller.output['pressure'])

    sat_temp = steamTable.tsat_p(curr_press)
    err = controller.pid(curr_temp)

    if sat_temp <= curr_temp:
        # Liquid to gas phase change
        pass

    else:
        # Liquid heating
        pass

    print(sat_temp)
    print(err)


@t2.job(interval=datetime.timedelta(milliseconds=200))
def savedata():
    if controller.data_save_started:
        print("Data save active.\n")

        SteamGenerator.objects.create(
            measurement_num = controller.curr_measurement_id,
            water_temp = controller.output['water_temp'],
            steam_temp_1 = controller.output['steam_temp_1'],
            steam_temp_2 = controller.output['steam_temp_2'],
            pressure = controller.output['pressure'],
            heater_water1_power = controller.output['heater_1'],
            heater_water2_power = controller.output['heater_2'],
            heater_water3_power = controller.output['heater_3'],
            heater_steam_power = controller.output['heater_st'],
            valve = controller.output['valve'],
            )

        SteamGenerator.save()

t1.start()
t2.start(block=True)