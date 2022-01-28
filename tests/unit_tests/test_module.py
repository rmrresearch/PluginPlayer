from pluginplayer import module
import unittest

class TestModule(unittest.TestCase):
    def setUp(self):
        self.default_state = {'callback_name' : None,
                              'callback' : None,
                              'citations' : [],
                              'description' : None,
                              'inputs' : {},
                              'property_types' : set(),
                              'results' : set(),
                              'submods' : {},
                             }

        self.nondefault_state = {'callback_name' : 'foo',
                                 'citations' : ['foo et al.'],
                                 'description' : 'Hello World!!!',
                                 'inputs' : {'input 0' : None, 'input 1' : 2},
                                 'property_types' : set('foo'),
                                 'results' : set('foo'),
                                 'submods' : {'callback 0' : module.Module()}
                                }


    def test_ctor(self):
        # Test the default ctor
        mod = module.Module()
        self.assertEqual(mod._unlocked, True)
        self.assertEqual(mod._cache, {})
        self.assertEqual(mod._is_memoizable, True)
        self.assertEqual(mod._state, self.default_state)

        # The following test each kwarg individually. Since we only change one
        # part of the default instance, if it is the same with the change and
        # different after reverting the change we can infer that the rest of the
        # state is the same.

        for k,v in self.nondefault_state.items():
            nondefault = module.Module(**{k : v})
            mod._state[k] = v
            self.assertEqual(mod, nondefault)
            mod._state[k] = self.default_state[k]
            self.assertNotEqual(mod, nondefault)


    def test_unlocked_copy(self):
        mod = module.Module()
        mod._unlocked = False

        a_copy = mod.unlocked_copy()
        self.assertFalse(a_copy.locked())

        mod._unlocked = True
        self.assertEqual(mod, a_copy)


    def test_has_module(self):
        mod = module.Module()
        self.assertFalse(mod.has_module())

        mod._state['callback'] = lambda inputs, submods : {}
        self.assertTrue(mod.has_module())


    def test_has_description(self):
        mod = module.Module()
        self.assertFalse(mod.has_description())

        mod._state['description'] = 'A description'
        self.assertTrue(mod.has_description())


    def test_locked(self):
        mod = module.Module()
        self.assertFalse(mod.locked())

        mod._unlocked = False
        self.assertTrue(mod.locked())

    def test_list_not_ready(self):
        pass


    def test_ready(self):
        pass


    def test_reset_cache(self):
        mod = module.Module()
        mod._cache['hello'] = 'world'

        mod.reset_cache()
        self.assertEqual(mod._cache, {})


    def test_is_memoizable(self):
        mod = module.Module()
        self.assertTrue(mod.is_memoizable())

        mod._is_memoizable = False
        self.assertFalse(mod.is_memoizable())


    def test_turn_off_memoization(self):
        mod = module.Module()
        mod.turn_off_memoization()
        self.assertFalse(mod._is_memoizable)

        # Calling it twice does nothing
        mod.turn_off_memoization()
        self.assertFalse(mod._is_memoizable)


    def test_turn_on_memoization(self):
        mod = module.Module()
        self.assertTrue(mod._is_memoizable)
        mod.turn_on_memoization()
        self.assertTrue(mod._is_memoizable)

        mod._is_memoizable = False
        mod.turn_on_memoization()
        self.assertTrue(mod._is_memoizable)


    def test_lock(self):
        mod = module.Module()
        mod.lock()
        self.assertTrue(mod.locked())

    def test_comparisons(self):

        lhs, rhs = module.Module(), module.Module()

        self.assertEqual(lhs, rhs)

        lhs._unlocked = False
        self.assertNotEqual(lhs, rhs)
        lhs._unlocked = True
        self.assertEqual(lhs, rhs)

        lhs._state['callback_name'] = 'hello_world'
        rhs._state['callback_name'] = 'foo_bar'
        self.assertNotEqual(lhs, rhs)
        lhs._state['callback_name'] = 'foo_bar'
        self.assertEqual(lhs, rhs)

        lhs._state['description'] = 'hello world'
        rhs._state['description'] = 'foo bar'
        self.assertNotEqual(lhs, rhs)
        lhs._state['description'] = 'foo bar'
        self.assertEqual(lhs, rhs)

        lhs._state['results'] = set('hello')
        rhs._state['results'] = set('bar')
        self.assertNotEqual(lhs, rhs)
        lhs._state['results'] = set('bar')
        self.assertEqual(lhs, rhs)

        lhs._state['inputs']['hello'] = 'bar'
        rhs._state['inputs']['hello'] = 'world'
        self.assertNotEqual(lhs, rhs)
        lhs._state['inputs']['hello'] = 'world'
        self.assertEqual(lhs, rhs)

        # TODO: Test Submods

        # TODO: Test property types

        lhs._state['citations'] = set('Foo et al.')
        rhs._state['citations'] = set('Bar et al.')
        self.assertNotEqual(lhs, rhs)
        lhs._state['citations'] = set('Bar et al.')
        self.assertEqual(lhs, rhs)
