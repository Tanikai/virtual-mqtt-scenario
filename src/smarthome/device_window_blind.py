import json
import tkinter as tk
from .device_base import DeviceBase, DeviceBaseView
from src import tools


class DeviceWindowBlindView(DeviceBaseView):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.l_device.config(text="Window Blind",
                             background=self.actuator_color)
        self.l_position = tk.Label(self, text="Current Position:")
        self.l_position.grid(row=self.row_offset, column=0, sticky=tk.W)
        self.l_valposition = tk.Label(self, text="CURRENT_POSITION")
        self.l_valposition.grid(row=self.row_offset, column=1, sticky=tk.W)

    def set_state(self, state: dict):
        super().set_state(state)
        if "position" in state:
            self.l_valposition.config(text=state["position"])


class DeviceWindowBlind(DeviceBase):

    def __init__(self, server_info: dict, home_id: str, room_id: str,
                 device_id: str):
        super().__init__(server_info, home_id, room_id, device_id)
        self.state = {"position": 1.0}
        self._position_topic = self.get_base_path() + "position"
        self._set_position_topic = self.get_base_path() + "set_position"

    def subscribe_controls(self):
        self.mqtt_client.subscribe(self._set_position_topic)

    def _client_message(self, client, userdata, msg):
        handled = super()._client_message(client, userdata, msg)
        if handled:
            return

        payload = self._decode_payload(msg.payload)

        if "value" not in payload:
            return

        if msg.topic == self._set_position_topic:
            self.set_position(payload["value"])

    def set_position(self, position: float):
        position = tools.clamp(position, 0.0, 1.0)
        if self.state["position"] != position:
            self.mqtt_client.publish(self._position_topic,
                                     json.dumps({"position": position}))
        self._set_new_value("position", position)
