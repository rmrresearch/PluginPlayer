import pluginplay as pp
import unittest

class PT0(pp.PropertyType):
    """Effective signature: result0 (input0)"""

    def __init__(self):
        inputs = [('input 0', None)]
        results = ['result 0']
        return super().__init__(inputs, results)


class TestModuleManager(unittest.TestCase):

    def setUp(self):
        pt   = PT0()
        fxn = lambda inputs, submods : {'result 0' : inputs['input 0']}
        self.mod0 = pp.Module(property_types=set([pt]), callback=fxn)


        sub_key = ('callback 0', pt)
        fxn     = lambda inputs, submods : submods[sub_key](inputs['input 0'])
        self.mod1 = pp.Module(property_types=set([pt]),
                              callback=fxn,
                              inputs={'input x' : 99},
                              submods={sub_key : None})
        self.mm = pp.ModuleManager()
        self.mm.add_module("Module 0", self.mod0)
        self.mm.add_module("Module 1", self.mod1)


    def test_contains(self):
        mm = self.mm
        # Has the key
        self.assertTrue('Module 0' in mm)
        self.assertFalse('Module 0' not in mm)

        # Doesn't have the key
        self.assertFalse('Not a key' in mm)
        self.assertTrue('Not a key' not in mm)


    def test_add_module(self):
        mm = self.mm

        # test_contains more or less tested correct usage, so just check errors
        self.assertRaises(KeyError, mm.add_module, 'Module 0', None)


    def test_getitem(self):
        mm = self.mm
        self.assertEqual(mm['Module 0'], self.mod0)
        self.assertEqual(mm['Module 1'], self.mod1)

        # Raises an error if there's no module
        self.assertRaises(KeyError, mm.__getitem__, 'not a key')


    def test_copy_module(self):
        mm = self.mm
        mm.copy_module('Module 0', 'Module 2')
        self.assertEqual(mm['Module 2'], self.mod0)

        # Raises an error if there's not module
        self.assertRaises(KeyError, mm.copy_module, 'not a key', ' Module 3')

        # Raises an error if there's already a module
        self.assertRaises(KeyError, mm.copy_module, 'Module 0', 'Module 1')


    def test_erase(self):
        mm = self.mm

        # Can erase a key
        mm.erase('Module 0')
        self.assertFalse('Module 0' in mm)

        # Can erase it multiple times w/o error
        mm.erase('Module 0')
        self.assertTrue('Module 0' not in mm)


    def test_rename_module(self):
        mm = self.mm

        # Raises an error if there's not module
        self.assertRaises(KeyError, mm.rename_module, 'not a key', ' Module 3')

        # Raises an error if there's already a module
        self.assertRaises(KeyError, mm.rename_module, 'Module 0', 'Module 1')

        mm.rename_module('Module 0', 'Module 2')
        self.assertEqual(mm['Module 2'], self.mod0)


    def test_change_input(self):
        mm = self.mm

        # Raises an error if module key is not valid
        self.assertRaises(KeyError, mm.change_input, 'not a key', 'input x', 42)

        # Raises an error if input key is not valid
        self.assertRaises(KeyError, mm.change_input, 'Module 1', 'not a key', 4)

        # Can change the input
        mm.change_input('Module 1', 'input x', 42)
        self.assertEqual(mm['Module 1'].inputs()['input x'], 42)
