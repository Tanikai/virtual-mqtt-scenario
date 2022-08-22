from unittest import TestCase
from .explorer import Explorer


class TestExplorer(TestCase):
    def test_insert_message(self):
        c = {}
        ex = Explorer(c)
        ex.insert_message("1/2", "test")
        self.assertEqual(len(ex.topictree["children"]["1"]["children"]), 1)
