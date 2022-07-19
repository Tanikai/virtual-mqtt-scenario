import json
from application import App
from smarthome.device_thermometer import DeviceThermometer, DeviceThermometerView
from smarthome.device_clock import DeviceClock, DeviceClockView
from smarthome.device_lamp import DeviceLamp, DeviceLampView
from smarthome.device_remote import DeviceRemote, DeviceRemoteView
from smarthome.device_window_blind import DeviceWindowBlind, \
    DeviceWindowBlindView


def remote_lights(self):
    self.mqtt_client.publish("home0/living_room/ceiling_lamp/set_power", json.dumps({"value": True}))


def init_clock(self):
    self.generator.set_time(15, 0)


if __name__ == '__main__':
    app = App()

    c = {
        "host": "localhost",
        "port": 1883,
        "keepalive": 60,
    }
    h0 = "home0"
    l = "living_room"

    # create new instance of DeviceThermometer, but only pass constructor
    d = app.add_device(DeviceClock(c, h0, "clock0"), DeviceClockView)
    d.on_run = init_clock
    app.add_device(DeviceThermometer(c, h0, l, "thermometer0"),
                   DeviceThermometerView)
    app.add_device(DeviceLamp(c, h0, l, "ceiling_lamp"), DeviceLampView)
    app.add_device(DeviceLamp(c, h0, l, "standing_lamp"), DeviceLampView)
    d = app.add_device(DeviceRemote(c, h0, l, "light_switch"),
                       DeviceRemoteView)
    d.set_text("Toggle Lights")
    d.on_click = remote_lights

    d = app.add_device(DeviceWindowBlind(c, h0, l, "window_blind"),
                       DeviceWindowBlindView)
    app.run()
