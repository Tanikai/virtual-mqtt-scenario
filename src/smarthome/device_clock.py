import tkinter as tk
from .device_base import DeviceBase, DeviceBaseView
from threading import Thread, Event
from datetime import datetime, time, timedelta, date


class DeviceClockView(DeviceBaseView):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.l_time = tk.Label(self, text="Current Time:")
        self.l_time.grid(row=self.row_offset, column=0, sticky=tk.W)
        self.l_valtime = tk.Label(self, text="VAL_TIME")
        self.l_valtime.grid(row=self.row_offset, column=1, sticky=tk.W)

    def set_state(self, state: dict):
        super().set_state(state)
        self.l_valtime.config(text=state["time"])


class ClockGenerator(Thread):

    callback = None
    current_time = datetime.combine(date.today(), time(hour=12))

    def __init__(self, callback):
        super().__init__(daemon=True)
        self.callback = callback
        self.event = Event()  # for stopping

    def run(self):
        while not self.event.is_set():
            self.callback({"time": self.current_time.strftime("%H:%M")})
            # increase 15 minutes every 1 second
            self.current_time = self.current_time + timedelta(minutes=15)
            self.event.wait(1)  # wait 1 second

    def stop(self):
        self.event.set()


class DeviceClock(DeviceBase):

    def __init__(self):
        super().__init__()
        self.generator = ClockGenerator(self._on_new_data)

    def _on_new_data(self, data: dict):
        handled = super()._on_new_data(data)
        if handled:
            return

        self.mqtt_client.publish(
            self.get_base_path() + "time",
            data["time"]
        )
        self._new_state(data)

