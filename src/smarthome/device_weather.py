import json
import tkinter as tk
from tkinter import ttk
from .device_base import DeviceBase, DeviceBaseView, GeneratorBase
import random
from src import tools


class DeviceWeatherView(DeviceBaseView):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.l_device.config(text="Weather Sensor",
                             background=self.sensor_color)
        self.l_weather = tk.Label(self, text="Current Weather:")
        self.l_weather.grid(row=self.row_offset, column=0, sticky=tk.W)
        self.l_valweather = tk.Label(self, text="VAL_WEATHER")
        self.l_valweather.grid(row=self.row_offset, column=1, sticky=tk.W)
        self.bt_newweather = tk.Button(self, text="Set Weather",
                                       command=self._bt_newweather_click)
        self.bt_newweather.grid(row=self.row_offset + 1, column=0, sticky=tk.W,
                                padx=2, pady=2)
        self.cb_newweather = ttk.Combobox(self)
        self.cb_newweather["values"] = ("clear", "cloudy", "rain")
        self.cb_newweather["state"] = "readonly"
        self.cb_newweather.grid(row=self.row_offset+1, column=1, sticky=tk.W)

        self.on_bt_weather_click = None

    def set_state(self, state: dict):
        super().set_state(state)
        if "weather" in state:
            self.l_valweather.config(text=state["weather"])

    def _bt_newweather_click(self):
        if self.on_bt_weather_click is None:
            return

        selected = self.cb_newweather.get()
        self.on_bt_weather_click(selected)


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

            self.event.wait(12)

    def set_weather(self, new_weather: str):
        print("set weather", new_weather)
        try:
            weather_index = self.weather_str.index(new_weather.lower())
        except ValueError as e:
            return  # do nothing when wrong input
        self.current_weather = weather_index
        self.callback({"weather": self.weather_str[self.current_weather]})

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

    def __init__(self, server_info: dict, home_id: str, device_id: str):
        super().__init__(server_info, home_id, "", device_id)
        self.generator = WeatherGenerator(self._on_new_data)
        self.state = {"weather": "sunny"}

    def set_view(self, view: DeviceWeatherView):
        super().set_view(view)
        view.on_bt_weather_click = self._on_set_weather

    def get_base_path(self) -> str:
        return f"{self.home_id}/{self.device_id}/"

    def _on_set_weather(self, weather: str):
        self.generator.set_weather(weather)

    def _on_new_data(self, data: dict):
        handled = super()._on_new_data(data)
        if handled:
            return

        if "weather" in data:
            weather_str = json.dumps({"weather": data["weather"]})
            self.mqtt_client.publish(
                self.get_base_path() + "weather", weather_str)

        self._new_state(data)
