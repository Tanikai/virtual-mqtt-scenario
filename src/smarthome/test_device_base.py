from unittest import TestCase
from .device_base import DeviceBase


class TestDeviceBase(TestCase):
    c = {
        "host": "localhost",
        "port": 1883,
        "keepalive": 60,
    }

    def test_get_base_path(self):
        device = DeviceBase(self.c, "house", "room", "myid123")
        self.assertEqual(device.get_base_path(), "house/room/myid123/")
