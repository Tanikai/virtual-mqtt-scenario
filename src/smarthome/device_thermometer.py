import json
import tkinter as tk
from random import randint
from .device_base import DeviceBase, DeviceBaseView, GeneratorBase


class DeviceThermometerView(DeviceBaseView):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.l_temp = tk.Label(self, text="Temperature:")
        self.l_temp.grid(row=self.row_offset, column=0, sticky=tk.W)
        self.l_valtemp = tk.Label(self, text="VAL_TEMPERATURE")
        self.l_valtemp.grid(row=self.row_offset, column=1, sticky=tk.W)
        self.l_humidity = tk.Label(self, text="Humidity:")
        self.l_humidity.grid(row=self.row_offset + 1, column=0, sticky=tk.W)
        self.l_valhumidity = tk.Label(self, text="VAL_HUMIDITY")
        self.l_valhumidity.grid(row=self.row_offset + 1, column=1, sticky=tk.W)

    def set_state(self, state: dict):
        super().set_state(state)
        if "temperature" in state:
            self.l_valtemp.config(text=state["temperature"])
        if "humidity" in state:
            self.l_valhumidity.config(text=state["humidity"])


class ThermometerGenerator(GeneratorBase):
    temp_upper = 30  # °C
    temp_lower = 15  # °C
    hum_upper = 90  # %
    hum_lower = 20  # %

    def __init__(self, callback):
        super().__init__(callback)
        # accuracy: 1 decimal
        self.last_temp = 20  # °C
        self.last_humidity = 75  # %

    def run(self):
        while not self.event.is_set():
            self.last_temp = self.generate_value(self.last_temp,
                                                 self.temp_lower,
                                                 self.temp_upper)
            self.last_humidity = self.generate_value(self.last_humidity,
                                                     self.hum_lower,
                                                     self.hum_upper)

            self.callback({"temperature": self.last_temp,
                           "humidity": self.last_humidity})
            self.event.wait(1)  # wait 1 sec

    @staticmethod
    def generate_value(last: float, lower: float, upper: float,
                       fluctuation=0.5) -> float:
        # move decimal point by 1 to right and round off rest
        def x(val):
            return round(val * 10)

        mul_last = x(last)
        mul_lower = x(lower)
        mul_upper = x(upper)
        mul_fluctuation = x(fluctuation)
        near_lower = mul_last - mul_fluctuation  # 0.5 °C fluctuation
        near_upper = mul_last + mul_fluctuation
        # if last is larger than upper, return upper
        rand_high = min(near_upper, mul_upper)
        # if last is smaller than lower, return lower
        rand_low = max(near_lower, mul_lower)

        # print(f"generate:[{rand_low},{rand_high}]")
        value = randint(rand_low, rand_high)  # bounds are inclusive
        return value / 10


class DeviceThermometer(DeviceBase):

    def __init__(self, server_info: dict, home_id: str, room_id: str,
                 device_id: str):
        super().__init__(server_info, home_id, room_id, device_id)
        self.generator = ThermometerGenerator(self._on_new_data)
        self.state = {"temperature": "20.0", "humidity": 75}

    def _on_new_data(self, data: dict):
        handled = super()._on_new_data(data)
        if handled:
            return

        if "temperature" in data:
            self.mqtt_client.publish(
                self.get_base_path() + "temperature",
                json.dumps({"temperature": data["temperature"]})
            )
        if "humidity" in data:
            self.mqtt_client.publish(
                self.get_base_path() + "humidity",
                json.dumps({"humidity": data["humidity"]})
            )
        self._new_state(data)
