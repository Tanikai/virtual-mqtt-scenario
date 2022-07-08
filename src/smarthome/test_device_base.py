from unittest import TestCase
import device_base


class TestDeviceBase(TestCase):

    def test_get_base_path(self):
        device = device_base.DeviceBase()
        self.assertEqual(device.get_base_path(), "/0/")
