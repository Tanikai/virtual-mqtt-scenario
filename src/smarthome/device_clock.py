import tkinter as tk
from .device_base import DeviceBase, DeviceBaseView
from threading import Thread, Event
from datetime import time, timedelta


class ClockGenerator(Thread):
    callback = None
    current_time = time(12, 0)

    def __init__(self, callback):
        super().__init__()
        self.callback = callback
        self.event = Event()  # for stopping

    def run(self):
        while not self.event.is_set():
            self.callback({"time": self.current_time.strftime("%H:%M")})
            # increase 15 minutes every 1 second
            self.current_time = self.current_time + timedelta(minutes=15)
            self.event.wait(1)  # wait 1 second


class DeviceClockView(DeviceBaseView):

    def __init__(self, parent=None):
        super().__init__(parent)


class DeviceClock(DeviceBase):
    generator = None

    def __init__(self):
        super().__init__()
