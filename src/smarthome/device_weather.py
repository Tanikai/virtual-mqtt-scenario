import json
import tkinter as tk
from .device_base import DeviceBase, DeviceBaseView, GeneratorBase
import random


class DeviceThermometerView(DeviceBaseView):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.l_weather = tk.Label(self, text="Current Weather:")
        self.l_weather.grid(row=self.row_offset, column=0, sticky=tk.W)
        self.l_valweather= tk.Label(self, text="VAL_WEATHER")
        self.l_valweather.grid(row=self.row_offset, column=1, sticky=tk.W)

    def set_state(self, state:dict):
        super().set_state(state)
        if "weather" in state:
            self.l_valweather.config(text=state["weather"])
            
            
class WeatherGenerator(GeneratorBase):
    weather_str = ["clear", "cloudy", "rain"]
    # transition probabilities
    weather_probs = [[0.6, 0.3, 0.1], [0.1, 0.3, 0.6], [0.4, 0.1, 0.5]]

    def __init__(self, callback):
        super().__init__(callback)
        self.current_weather = 0

    def run(self):
        while not self.event.is_set():
            self.current_weather = self.next_weather(self.current_weather)
            self.callback({"weather": self.weather_str[self.current_weather]})
            self.event.wait(10)

    def next_weather(self, current_weather: int) -> int:
        # w is the weather today
        cpd = random.random()
        current_probs = self.weather_probs[current_weather]
        for index, weather_prob in enumerate(current_probs):
            cpd -= weather_prob
            if cpd <= 0:
                return index
        # if not returned before: sum of probabilities are less than 1
        raise ValueError("probabilities of transitions add up to less than 1")


class DeviceWeather(DeviceBase):

    def __init__(self, server_info: dict, home_id: str, room_id: str,
                 device_id: str):
        super().__init__(server_info, home_id, room_id, device_id)
        self.generator = WeatherGenerator(self._on_new_data)
        self.state = {"weather": "sunny"}

    def _on_new_data(self, data: dict):
        if self.on_new_data is not None:
            self.on_new_data(data)
            return

        if "weather" in data:
            self.mqtt_client.publish(self.get_base_path() + "weather"),
            json.dumps({"weather": data["weather"]})

        self._new_state(data)
