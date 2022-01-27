from pluginplayer import module
import unittest

class TestModule(unittest.TestCase):

    def test_has_description(self):
        mod = module.Module()
        self.assertFalse(mod.has_description())
