import json
import tkinter as tk
from .device_base import DeviceBase, DeviceBaseView


class DeviceWindowView(DeviceBaseView):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.l_device.config(text="Window", background=self.actuator_color)
        self.l_opened = tk.Label(self, text="Currently Open:")
        self.l_opened.grid(row=self.row_offset, column=0, sticky=tk.W)
        self.l_valopened = tk.Label(self, text="OPENED_STATUS")
        self.l_valopened.grid(row=self.row_offset, column=1, sticky=tk.W)

    def set_state(self, state: dict):
        super().set_state(state)
        if "opened" in state:
            if state["opened"]:
                self.l_valopened.config(text="Open", background="green")
            else:
                self.l_valopened.config(text="Closed", background="red")


class DeviceWindow(DeviceBase):

    def __init__(self, server_info: dict, home_id: str, room_id: str,
                 device_id: str):
        super().__init__(server_info, home_id, room_id, device_id)
        self.state = {"opened": False}
        self._opened_topic = self.get_base_path() + "opened"
        self._set_opened_topic = self.get_base_path() + "set_opened"
        self._toggle_opened_topic = self.get_base_path() + "toggle_opened"

    def subscribe_controls(self):
        self.mqtt_client.subscribe(self._set_opened_topic)

    def _client_message(self, client, userdata, msg):
        handled = super()._client_message(client, userdata, msg)
        if handled:
            return

        payload = self._decode_payload(msg.payload)

        if msg.topic == self._toggle_opened_topic:
            self.set_opened(not self.state["opened"])

        if "value" not in payload:
            return

        if msg.topic == self._set_opened_topic:
            self.set_opened(payload["value"])

    def set_opened(self, opened: bool):
        if self.state["opened"] is not opened:
            self.mqtt_client.publish(self._opened_topic,
                                     json.dumps({"opened": opened}))
        self._set_new_value("opened", opened)
