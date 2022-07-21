from unittest import TestCase
from explorer import Explorer


class TestExplorer(TestCase):
    def test_insert_message(self):
        ex = Explorer()
        ex.insert_message("/1/2", "test")
        self.fail()
