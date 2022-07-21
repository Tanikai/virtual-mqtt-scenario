import json
from application import App
import configparser
import sys
from os.path import exists
from os import getcwd
from smarthome.device_thermometer import DeviceThermometer, \
    DeviceThermometerView
from smarthome.device_clock import DeviceClock, DeviceClockView
from smarthome.device_lamp import DeviceLamp, DeviceLampView
from smarthome.device_remote import DeviceRemote, DeviceRemoteView
from smarthome.device_window_blind import DeviceWindowBlind, \
    DeviceWindowBlindView
from smarthome.device_window import DeviceWindow, DeviceWindowView
from smarthome.device_weather import DeviceWeather, DeviceWeatherView


def remote_lights(self):
    self.mqtt_client.publish("home0/living_room/ceiling_lamp/toggle_power",
                             json.dumps({"sender": "remote"}))


def init_clock(self):
    self.generator.set_time(15, 0)


def read_config_file(path: str) -> dict:
    parser = configparser.ConfigParser()
    parser.read(path)

    config = {}
    section = "mqtt broker"
    config["host"] = parser.get(section, "host")
    config["port"] = int(parser.get(section, "port"))
    config["keepalive"] = int(parser.get(section, "keepalive"))

    return config


def get_config_dict() -> dict:
    if len(sys.argv) >= 2:  # If env file is passed
        config_name = sys.argv[1]
    else:
        config_name = getcwd() + "/default.ini"
        if not exists(config_name):
            config_name = getcwd() + "/localhost.ini"

    return read_config_file(config_name)


if __name__ == '__main__':
    app = App()

    c = get_config_dict()

    h0 = "home0"
    l = "living_room"
    act_col = 1  # actuator column

    # create new instance of DeviceThermometer, but only pass constructor
    clock = DeviceClock(c, h0, "clock0")
    clock.on_run = init_clock
    app.add_device(clock, DeviceClockView)
    app.add_device(DeviceThermometer(c, h0, l, "thermometer0"),
                   DeviceThermometerView)
    app.add_device(DeviceLamp(c, h0, l, "ceiling_lamp"), DeviceLampView, act_col)
    app.add_device(DeviceLamp(c, h0, l, "standing_lamp"), DeviceLampView, act_col)
    d = app.add_device(DeviceRemote(c, h0, l, "light_switch"),
                       DeviceRemoteView)
    d.set_text("Toggle Lights")
    d.on_click = remote_lights

    app.add_device(DeviceWindow(c, h0, l, "window0"), DeviceWindowView, act_col)
    app.add_device(DeviceWindowBlind(c, h0, l, "window_blind"),
                   DeviceWindowBlindView, act_col)
    app.add_device(DeviceWeather(c, h0, "weather_sensor0"), DeviceWeatherView)
    app.run()
