import tkinter as tk
from .device_base import DeviceBase, DeviceBaseView
from threading import Thread


class ClockGenerator(Thread):

    def __init__(self, callback):
        super().__init__()

    def run(self):
        while not self.event_is_set():
            




class DeviceClockView(DeviceBaseView):

    def __init__(self, parent=None):
        super().__init__(parent)


class DeviceClock(DeviceBase):
    generator = None

    def __init__(self):
        super().__init__()

    d