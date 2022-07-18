import tkinter as tk
from random import randint
from .device_base import DeviceBase, DeviceBaseView, GeneratorBase


class DeviceThermostatView(DeviceBaseView):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.l_temp = tk.Label(self, text="Temperature:")
        self.l_temp.grid(row=self.row_offset, column=0, sticky=tk.W)
        self.l_valtemp = tk.Label(self, text="VAL_TEMPERATURE")
        self.l_valtemp.grid(row=self.row_offset, column=1, sticky=tk.W)

    def set_state(self, state: dict):
        super().set_state(state)
        self.l_valtemp.config(text=state["temperature"])


class ThermostatGenerator(GeneratorBase):

    def __init__(self, callback):
        super().__init__(callback)
        self.last_reading = 20

    def run(self):
        while not self.event.is_set():
            self.last_reading = self.generate_room_temperature(
                self.last_reading)
            # print(self.last_reading)
            self.callback({"temperature": self.last_reading})
            self.event.wait(1)  # wait 1 sec

    @staticmethod
    def generate_room_temperature(last=20.0) -> float:
        last = int(last) * 10
        temp = randint(last - 10, last + 11)
        return temp / 10


class DeviceThermostat(DeviceBase):

    def __init__(self, server_info: dict, home_id: str, room_id: str,
                 device_id: str):
        super().__init__(server_info, home_id, room_id, device_id)
        self.generator = ThermostatGenerator(self._on_new_data)
        self.state = {"temperature": "20.0"}

    def _on_new_data(self, data: dict):
        if self.on_new_data is not None:
            self.on_new_data(data)
            return

        self.mqtt_client.publish(
            self.get_base_path() + "temperature",
            data["temperature"]
        )
        self._new_state(data)
