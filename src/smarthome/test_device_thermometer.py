from unittest import TestCase
import device_thermometer
from time import sleep


class TestDeviceThermometer(TestCase):

    def test_thermometer_generator(self):
        th = device_thermometer.ThermometerGenerator(None)
        th.start()
        sleep(10)
        th.event.set()
