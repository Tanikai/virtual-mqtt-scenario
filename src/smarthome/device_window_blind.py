import json
import tkinter as tk
from .device_base import DeviceBase, DeviceBaseView


class DeviceWindowBlindView(DeviceBaseView):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.l_position = tk.Label(self, text="Current Position:")
        self.l_position.grid(row=self.row_offset, column=0, sticky=tk.W)
        self.l_valposition = tk.Label(self, text="CURRENT_POSITION")
        self.l_valposition.grid(row=self.row_offset, column=1, sticky=tk.W)

    def set_state(self, state: dict):
        super().set_state(state)
        self.l_valposition.config(text=state["position"])


class DeviceWindowBlind(DeviceBase):

    def __init__(self, server_info: dict, home_id: str, room_id: str,
             device_id: str):
        super().__init__(server_info, home_id, room_id, device_id)
        self.state = {"position": 1.0}
        self._set_position_topic = self.get_base_path() + "set_position"

    def subscribe_controls(self):
        self.mqtt_client.subscribe(self._set_position_topic)

    def _client_message(self, client, userdata, msg):
        if self.on_message is not None:
            self.on_message(self, client, userdata, msg)
            return

        payload_str = str(msg.payload.decode("utf-8"))
        payload = json.loads(payload_str)

        if msg.topic == self._set_position_topic:
            self.set_position(payload["value"])

    def set_position(self, position: float):
        new = self.state.copy()
        if position > 1.0:
            position = 1.0
        elif position < 0.0:
            position = 0.0
        new["position"] = position
        self._new_state(new)

