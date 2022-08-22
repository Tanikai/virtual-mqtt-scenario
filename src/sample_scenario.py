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
from smarthome.device_radiator import DeviceRadiator, DeviceRadiatorView
import json

home_id = "home0"


def _init_clock(self):
    self.generator.set_time(15, 0)


def init_living_room(app: App, c: dict):
    room_id = "living_room"

    # Thermometer
    app.add_device(DeviceThermometer(c, home_id, room_id, "thermometer"),
                   DeviceThermometerView, 1)

    # Ceiling Lamp
    app.add_device(DeviceLamp(c, home_id, room_id, "ceiling_lamp"),
                   DeviceLampView, 1)

    # Standing Lamp
    app.add_device(DeviceLamp(c, home_id, room_id, "standing_lamp"),
                   DeviceLampView, 1)

    # Lamp Remote
    d = app.add_device(DeviceRemote(c, home_id, room_id, "light_switch"),
                       DeviceRemoteView, 1)
    d.set_text("Toggle Lights")

    def _remote_lights(self, user_input: str):
        self.mqtt_client.publish(
            f"{home_id}/{room_id}/ceiling_lamp/toggle_power",
            json.dumps({"sender": "remote"}))

    d.on_click = _remote_lights

    # Window
    app.add_device(DeviceWindow(c, home_id, room_id, "window0"),
                   DeviceWindowView, 1)

    app.add_device(DeviceWindowBlind(c, home_id, room_id, "window_blind"),
                   DeviceWindowBlindView, 1)

    # Light switch to turn off all devices
    r = DeviceRemote(c, home_id, room_id, "light_switch_off_all")

    def turn_off_all_lights(self, user_input: str):
        off_msg = json.dumps({"value": False})
        self.mqtt_client.publish(
            f"{home_id}/living_room/ceiling_lamp/set_power", off_msg)
        self.mqtt_client.publish(
            f"{home_id}/living_room/standing_lamp/set_power", off_msg)
        self.mqtt_client.publish(f"{home_id}/bathroom/ceiling_lamp/set_power",
                                 off_msg)

    r.on_click = turn_off_all_lights
    app.add_device(r, DeviceRemoteView)
    r.set_text("Turn off all")


def init_bedroom(app: App, c: dict):
    room_id = "bedroom"

    # Thermometer
    app.add_device(
        DeviceThermometer(c, home_id, room_id, "thermometer"),
        DeviceThermometerView, 2)

    # Ceiling Lamp
    app.add_device(DeviceLamp(c, home_id, room_id, "ceiling_lamp"),
                   DeviceLampView, 2)

    # Lamp Remote
    lamp_remote = DeviceRemote(c, home_id, room_id, "light_switch")

    def _lamp_remote_clicked(self, input: str):
        self.mqtt_client.publish(
            f"{home_id}/{room_id}/ceiling_lamp/toggle_power", json.dumps({}))

    lamp_remote.on_click = _lamp_remote_clicked
    app.add_device(lamp_remote, DeviceRemoteView, 2)
    lamp_remote.set_text("Toggle Light")

    # Window
    app.add_device(DeviceWindow(c, home_id, room_id, "window"),
                   DeviceWindowView, 2)

    # Window Blind
    app.add_device(
        DeviceWindowBlind(c, home_id, room_id, "window_blinds"),
        DeviceWindowBlindView, 2)

    # Radiator
    app.add_device(
        DeviceRadiator(c, home_id, room_id, "radiator"),
        DeviceRadiatorView, 2)


def init_bathroom(app: App, c: dict):
    room_id = "bathroom"

    # Thermometer
    app.add_device(
        DeviceThermometer(c, home_id, room_id, "thermometer"),
        DeviceThermometerView, 3)

    # Ceiling Lamp
    app.add_device(DeviceLamp(c, home_id, room_id, "ceiling_lamp"),
                   DeviceLampView, 3)

    # Mirror Lamp
    mirror_lamp = DeviceLamp(c, home_id, room_id, "mirror_lamp")

    def mirror_lamp_subscribe(self):
        self.mqtt_client.subscribe(f"{home_id}/{room_id}/ceiling_lamp/power")

    mirror_lamp.on_run = mirror_lamp_subscribe

    def mirror_lamp_on_message(self, client, userdata, msg) -> bool:
        handled = False
        payload = self._decode_payload(msg.payload)
        if msg.topic == f"{home_id}/{room_id}/ceiling_lamp/power":
            self.set_power(payload["power"])
            handled = True
        return handled

    mirror_lamp.on_message = mirror_lamp_on_message
    app.add_device(mirror_lamp, DeviceLampView, 3)

    # Remote Control for Lamp
    lamp_remote = DeviceRemote(c, home_id, room_id, "light_switch")

    def _lamp_remote_clicked(self, input: str):
        self.mqtt_client.publish(
            f"{home_id}/{room_id}/ceiling_lamp/toggle_power", json.dumps({}))

    lamp_remote.on_click = _lamp_remote_clicked
    app.add_device(lamp_remote, DeviceRemoteView, 3)
    lamp_remote.set_text("Toggle Light")

    # Automatic Window: Opens when humidity is too high
    window = DeviceWindow(c, home_id, room_id, "window")
    app.add_device(window, DeviceWindowView, 3)

    def window_subscribe(self):
        self.mqtt_client.subscribe(f"{home_id}/{room_id}/thermometer/humidity")

    window.on_run = window_subscribe

    def window_on_message(self, client, userdata, msg) -> bool:
        handled = False
        payload = self._decode_payload(msg.payload)
        if msg.topic == f"{home_id}/{room_id}/thermometer/humidity":
            humidity = float(payload["humidity"])
            if humidity > 60:  # alternatively: set_opened(humidity > 60)
                self.set_opened(True)
            else:
                self.set_opened(False)
            handled = True
        return handled

    window.on_message = window_on_message

    # Radiator
    app.add_device(DeviceRadiator(c, home_id, room_id, "towel_radiator"),
                   DeviceRadiatorView, 3)

    # Radiator Remote
    r = DeviceRemote(c, home_id, room_id, "radiator_control", with_input=True)

    def _bathroom_radiator_control_clicked(self, input: str):
        try:
            new_radiator_temp = float(input)
        except Exception as e:
            print("user input is not float:", e)
            return

        self.mqtt_client.publish(
            f"{home_id}/{room_id}/towel_radiator/set_temperature",
            json.dumps({"value": new_radiator_temp}))

    r.on_click = _bathroom_radiator_control_clicked
    app.add_device(r, DeviceRemoteView, 3)
    r.set_text("Set Radiator Temp")


def init_house(app: App, c: dict):
    clock = DeviceClock(c, home_id, "clock")
    clock.on_run = _init_clock
    app.add_device(clock, DeviceClockView, 0)
    app.add_device(DeviceWeather(c, home_id, "weather_sensor"),
                   DeviceWeatherView, 0)


def init_sample_scenario(app: App, c: dict):
    """
    Creates a sample smart home scenario.
    :param app: Application object
    :param c: MQTT Broker configuration
    :return:
    """
    # create new instance of DeviceThermometer, but only pass constructor
    init_house(app, c)
    init_living_room(app, c)
    init_bedroom(app, c)
    init_bathroom(app, c)
