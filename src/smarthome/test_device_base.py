from unittest import TestCase
import device_base


class TestDeviceBase(TestCase):
    c = {
        "host": "localhost",
        "port": 1883,
        "keepalive": 60,
    }

    def test_get_base_path(self):
        device = device_base.DeviceBase(self.c, "house", "room", "myid123")
        self.assertEqual(device.get_base_path(), "house/room/myid123/")
