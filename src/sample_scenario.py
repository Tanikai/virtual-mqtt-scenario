from application import App
from smarthome.device_thermometer import DeviceThermometer, \
    DeviceThermometerView
from smarthome.device_clock import DeviceClock, DeviceClockView
from smarthome.device_lamp import DeviceLamp, DeviceLampView
from smarthome.device_remote import DeviceRemote, DeviceRemoteView
from smarthome.device_window_blind import DeviceWindowBlind, \
    DeviceWindowBlindView
from smarthome.device_window import DeviceWindow, DeviceWindowView
from smarthome.device_weather import DeviceWeather, DeviceWeatherView
import json


def _remote_lights(self):
    self.mqtt_client.publish("home0/living_room/ceiling_lamp/toggle_power",
                             json.dumps({"sender": "remote"}))


def _init_clock(self):
    self.generator.set_time(15, 0)


def init_sample_scenario(app: App, c: dict):
    """
    Creates a sample smart home scenario.
    :param app: Application object
    :param c: MQTT Broker configuration
    :return:
    """
    h0 = "home0"
    l_room = "living_room"
    act_col = 1  # actuator column
    clock = DeviceClock(c, h0, "clock0")
    clock.on_run = _init_clock
    # create new instance of DeviceThermometer, but only pass constructor
    app.add_device(clock, DeviceClockView)
    app.add_device(DeviceThermometer(c, h0, l_room, "thermometer0"),
                   DeviceThermometerView)
    app.add_device(DeviceLamp(c, h0, l_room, "ceiling_lamp"), DeviceLampView,
                   act_col)
    app.add_device(DeviceLamp(c, h0, l_room, "standing_lamp"), DeviceLampView,
                   act_col)
    d = app.add_device(DeviceRemote(c, h0, l_room, "light_switch"),
                       DeviceRemoteView)
    d.set_text("Toggle Lights")
    d.on_click = _remote_lights

    app.add_device(DeviceWindow(c, h0, l_room, "window0"), DeviceWindowView,
                   act_col)
    app.add_device(DeviceWindowBlind(c, h0, l_room, "window_blind"),
                   DeviceWindowBlindView, act_col)
    app.add_device(DeviceWeather(c, h0, "weather_sensor0"), DeviceWeatherView)
