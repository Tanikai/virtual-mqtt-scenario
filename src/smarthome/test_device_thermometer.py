from unittest import TestCase
from .device_thermometer import ThermometerGenerator
from time import sleep


class TestDeviceThermometer(TestCase):

    def test_thermometer_generator(self):
        data_list = []
        def thermo_callback(data):
            data_list.append(data)
        th = ThermometerGenerator(thermo_callback)
        th.start()
        sleep(3.5)
        th.event.set()
        self.assertEqual(len(data_list), 4)
