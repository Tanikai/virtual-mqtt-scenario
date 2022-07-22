import json
import tkinter as tk
from .device_base import DeviceBase, DeviceBaseView, GeneratorBase
from datetime import datetime, time, timedelta, date
from src import tools


class DeviceClockView(DeviceBaseView):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.l_device.config(text="Clock", background=self.sensor_color)
        self.l_time = tk.Label(self, text="Current Time:")
        self.l_time.grid(row=self.row_offset, column=0, sticky=tk.W)
        self.l_valtime = tk.Label(self, text="VAL_TIME")
        self.l_valtime.grid(row=self.row_offset, column=1, sticky=tk.W)
        self.bt_newtime = tk.Button(self, text="Set Time",
                                    command=self._bt_newtime_click)
        self.bt_newtime.grid(row=self.row_offset + 1, column=0, sticky=tk.W,
                             padx=2, pady=2)
        self.e_newtime = tk.Entry(self)
        self.e_newtime.insert(0, "12:00")
        self.e_newtime.grid(row=self.row_offset + 1, column=1, sticky=tk.W)
        self.on_bt_time_click = None

    def set_state(self, state: dict):
        super().set_state(state)
        self.l_valtime.config(text=state["time"])

    def _bt_newtime_click(self):
        if self.on_bt_time_click is None:
            return

        try:
            new_time = self.e_newtime.get().split(":")
            hour = int(new_time[0])
            minute = int(new_time[1])
            self.on_bt_time_click(hour, minute)
        except Exception as e:
            print(e)


class ClockGenerator(GeneratorBase):

    def __init__(self, callback):
        super().__init__(callback)
        # datetime object is used to wrap overflow from 23:59 to 00:00
        # https://bugs.python.org/issue1487389
        self.current_time = datetime.combine(date.today(), time(hour=12))

    def set_time(self, new_hour=12, new_minute=0):
        hour = tools.clamp(new_hour, 0, 23)
        minute = tools.clamp(new_minute, 0, 59)
        self.current_time = datetime.combine(
            date.today(), time(hour=hour, minute=minute))
        self.callback({"time": self.current_time.strftime("%H:%M")})

    def run(self):
        while not self.event.is_set():
            self.callback({"time": self.current_time.strftime("%H:%M")})
            # increase 15 minutes every 1 second
            self.current_time = self.current_time + timedelta(minutes=15)
            self.event.wait(1)  # wait 1 second


class DeviceClock(DeviceBase):

    def __init__(self, server_info, home_id, device_id):
        super().__init__(server_info, home_id, "", device_id)
        self.generator = ClockGenerator(self._on_new_data)
        self.state = {"time": "12:00"}

    def set_view(self, view: DeviceClockView):
        super().set_view(view)
        view.on_bt_time_click = self._on_set_time

    def get_base_path(self) -> str:
        return f"{self.home_id}/{self.device_id}/"

    def _on_set_time(self, hour, minute: int):
        self.generator.set_time(hour, minute)

    def _on_new_data(self, data: dict):
        handled = super()._on_new_data(data)
        if handled:
            return

        self.mqtt_client.publish(self.get_base_path() + "time",
                                 json.dumps({"time": data["time"]}))
        self._new_state(data)
