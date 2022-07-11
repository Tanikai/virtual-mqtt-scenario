from unittest import TestCase
import device_thermostat
from time import sleep


class TestDeviceThermostat(TestCase):

    def test_thermostat_generator(self):
        th = device_thermostat.ThermostatGenerator(None)
        th.start()
        sleep(10)
        th.event.set()
