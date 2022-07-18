import tkinter as tk
from .device_base import DeviceBase, DeviceBaseView, GeneratorBase


class DeviceRemoteView(DeviceBaseView):

    def __init__(self, parent=None, bt_callback=None):
        super().__init__(parent)
        self.bt_remote = tk.Button(self, text="", command=bt_callback)
        self.bt_remote.grid(row=self.row_offset, column=1, sticky=tk.W)
        self.on_click = bt_callback

    def set_button_text(self, button_text="REMOTE"):
        self.bt_remote.config(text=button_text)

    def set_button_callback(self, button_callback):
        self.bt_remote.config(command=button_callback)


class DeviceRemote(DeviceBase):

    def __init__(self, server_info: dict, home_id: str, room_id: str,
                 device_id: str):
        super().__init__(server_info, home_id, room_id, device_id)
        self.on_click = None

    def set_text(self, text: str):
        self.view.set_button_text(text)

    def set_view(self, view: DeviceRemoteView):
        super().set_view(view)
        view.set_button_callback(self._on_click)

    def _on_click(self):
        if self.on_click is not None:
            self.on_click(self)
