import threading

import device_base
from threading import Thread
from random import randint


class ThermostatGenerator(Thread):
    callback = None
    last_reading = 20

    def __init__(self, callback):
        super().__init__()
        self.callback = callback  # callback method when generating new value
        self.event = threading.Event()  # for stopping generator

    def run(self):
        while not self.event.is_set():
            self.last_reading = self.generate_room_temperature(self.last_reading)
            print(self.last_reading)
            self.event.wait(1)  # wait 1 sec

    @staticmethod
    def generate_room_temperature(last=20) -> float:
        last = int(last) * 10
        temp = randint(last - 10, last + 11)
        return temp / 10


class DeviceThermostat(device_base.DeviceBase):

    def __init__(self):
        super().__init__()
