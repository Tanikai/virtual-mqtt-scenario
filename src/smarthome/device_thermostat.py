from threading import Thread, Event
from random import randint
from .device_base import DeviceBase


class ThermostatGenerator(Thread):
    callback = None
    last_reading = 20

    def __init__(self, callback):
        super().__init__()
        self.callback = callback  # callback method when generating new value
        self.event = Event()  # for stopping generator

    def run(self):
        while not self.event.is_set():
            self.last_reading = self.generate_room_temperature(self.last_reading)
            # print(self.last_reading)
            self.callback({"temperature": self.last_reading})
            self.event.wait(1)  # wait 1 sec

    @staticmethod
    def generate_room_temperature(last=20.0) -> float:
        last = int(last) * 10
        temp = randint(last - 10, last + 11)
        return temp / 10


class DeviceThermostat(DeviceBase):
    generator = None

    def on_new_data(self, data: dict):
        self.mqtt_client.publish(
            self.get_base_path() + "temperature",
            data["temperature"]
        )

    def __init__(self):
        super().__init__()
        self.generator = ThermostatGenerator(self.on_new_data)

    def __del__(self):
        self.generator.event.set()
        super().__del__()

    def run(self):
        super().run()
        self.generator.start()

    def stop(self):
        self.generator.event.set()

    def on_connect(self, client, userdata, flags, rc):
        print("Thermostat connected")


