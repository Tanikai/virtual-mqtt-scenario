import tkinter as tk
from .device_base import DeviceBase, DeviceBaseView


class DeviceRemoteView(DeviceBaseView):

    def __init__(self, parent=None, bt_callback=None, with_input=False):
        super().__init__(parent)
        self.l_lastchange.grid_forget()  # do not use last change for remote
        self.l_vallastchange.grid_forget()
        self.l_device.config(text="Remote", background=self.sensor_color)

        self.bt_remote = tk.Button(self, text="", command=self._bt_click)
        self.bt_remote.grid(row=self.row_offset, column=0, sticky=tk.W)

        self.on_bt_click = bt_callback

        self.e_input = tk.Entry(self)
        self.has_input = with_input
        self.set_input_visible(with_input)

    def set_button_text(self, button_text="REMOTE"):
        self.bt_remote.config(text=button_text)

    def _bt_click(self):
        if self.on_bt_click is None:
            return
        try:
            self.on_bt_click(self.get_input_text())
        except Exception as e:
            print(e)

    def get_input_text(self) -> str:
        return self.e_input.get()

    def set_input_visible(self, show_input: bool):
        # if input visibility is already fulfilled
        if show_input:
            self.e_input.grid(row=self.row_offset, column=1, sticky=tk.W)
        else:
            self.e_input.grid_forget()


class DeviceRemote(DeviceBase):

    def __init__(self, server_info: dict, home_id: str, room_id: str,
                 device_id: str, with_input=False):
        super().__init__(server_info, home_id, room_id, device_id)
        self.on_click = None
        self.with_input = with_input

    def set_text(self, text: str):
        self.view.set_button_text(text)

    def set_view(self, view: DeviceRemoteView):
        super().set_view(view)
        view.set_input_visible(self.with_input)
        view.on_bt_click = self._on_click

    def _on_click(self, user_input: str):
        if self.on_click is not None:
            self.on_click(self, user_input)
