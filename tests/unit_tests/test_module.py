import pluginplay as pp
import unittest

class PT0(pp.PropertyType):
    """Effective signature: result0 (input0)"""

    def __init__(self):
        inputs = [('input 0', None)]
        results = ['result 0']
        return super().__init__(inputs, results)




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
                                 'inputs' : {'input x' : None},
                                 'property_types' : set([PT0()]),
                                 'results' : set(['result x']),
                                 'submods' : {('callback 0', PT0()) : None}
                                }

        fxn = lambda inputs, submods : {'result 0' : inputs['input 0'] }

        # This module is ready and can be run
        self.ready_submod  = pp.Module(property_types=set([PT0()]))
        self.ready_submod._state['callback'] = fxn

        # This module is not ready because 'input x' isn't set
        self.not_ready_submod = pp.Module(inputs= {'input x' : None },
                                          property_types=set([PT0()]))
        self.not_ready_submod._state['callback'] = fxn

        # This module isn't ready because 'input x' and 'callback 0' aren't set
        fxn = lambda inputs, submods : submods[('callback 0', PT0())](42)
        self.nondefault_mod = pp.Module(**self.nondefault_state)
        self.nondefault_mod._state['callback'] = fxn


    def test_ctor(self):
        # Test the default ctor
        mod = pp.Module()
        self.assertEqual(mod._unlocked, True)
        self.assertEqual(mod._cache, {})
        self.assertEqual(mod._is_memoizable, True)
        self.assertEqual(mod._state, self.default_state)

        # The following test each kwarg individually. Since we only change one
        # part of the default instance, if it is the same with the change and
        # different after reverting the change we can infer that the rest of the
        # state is the same.

        for k,v in self.nondefault_state.items():
            nondefault = pp.Module(**{k : v})
            mod._state[k] = v
            self.assertEqual(mod, nondefault)
            mod._state[k] = self.default_state[k]
            self.assertNotEqual(mod, nondefault)


    def test_unlocked_copy(self):
        mod = pp.Module()
        mod._unlocked = False

        a_copy = mod.unlocked_copy()
        self.assertFalse(a_copy.locked())

        mod._unlocked = True
        self.assertEqual(mod, a_copy)


    def test_has_module(self):
        mod = pp.Module()
        self.assertFalse(mod.has_module())

        mod = self.ready_submod
        self.assertTrue(mod.has_module())


    def test_has_description(self):
        # Calling on a default module raises an exception
        mod = pp.Module()
        self.assertRaises(RuntimeError, mod.has_description)

        # With a callable, but no description
        mod = self.ready_submod
        self.assertFalse(mod.has_description())

        # With a callable, and a description
        mod._state['description'] = 'A description'
        self.assertTrue(mod.has_description())


    def test_locked(self):
        mod = pp.Module()
        self.assertFalse(mod.locked())

        mod._unlocked = False
        self.assertTrue(mod.locked())


    def test_list_not_ready(self):
        # Calling a default module raises an exception
        mod0 = pp.Module()
        self.assertRaises(RuntimeError, mod0.list_not_ready)

        # Ready, but still shows the input for the PT
        mod0 =self.ready_submod
        corr = {'Inputs' : set(['input 0']), 'Submodules' : set()}
        self.assertEqual(mod0.list_not_ready(), corr)

        # Not ready because inputs aren't set
        mod1 = self.not_ready_submod
        corr = {'Inputs' : set(['input x', 'input 0']), 'Submodules' : set()}
        self.assertEqual(mod1.list_not_ready(), corr)

        # Not ready b/c inputs and a submodule aren't set
        mod2 = self.nondefault_mod
        corr = {'Inputs' : set(['input x','input 0']),
                'Submodules' : set(['callback 0'])}
        self.assertEqual(mod2.list_not_ready(), corr)

        # Not ready b/c submodule isn't ready
        mod2._state['submods'][('callback 0', PT0())] = self.not_ready_submod
        self.assertEqual(mod2.list_not_ready(), corr)

        # Setting submodule to a ready one removes it from the list
        mod2._state['submods'][('callback 0', PT0())] = self.ready_submod
        corr = {'Inputs' : set(['input x', 'input 0']), 'Submodules' : set()}
        self.assertEqual(mod2.list_not_ready(), corr)


    def test_ready(self):
        pt = PT0()

        # Calling a default module raises an exception
        mod0 = pp.Module()
        self.assertRaises(RuntimeError, mod0.ready, pt)

        # Not ready b/c 'input x' isn't set
        mod1 = self.not_ready_submod
        self.assertFalse(mod1.ready(pt))
        mod1._state['inputs']['input x'] = 42
        self.assertTrue(mod1.ready(pt))

        # The ready submod is actually ready
        mod2 = self.ready_submod
        self.assertTrue(mod2.ready(pt))

        # Not ready b/c 'input x' and 'callback 0' isn't set
        mod3 = self.nondefault_mod
        self.assertFalse(mod3.ready(pt))
        mod3._state['inputs']['input x'] = 42
        self.assertFalse(mod3.ready(pt))
        mod3._state['submods'][('callback 0', pt)] = self.ready_submod
        self.assertTrue(mod3.ready(pt))


    def test_reset_cache(self):
        mod = pp.Module()
        mod._cache['hello'] = 'world'

        mod.reset_cache()
        self.assertEqual(mod._cache, {})


    def test_is_memoizable(self):
        # Default module raises an exception
        mod = pp.Module()
        self.assertRaises(RuntimeError, mod.is_memoizable)

        mod0 = self.nondefault_mod
        self.assertTrue(mod0.is_memoizable())

        mod0._is_memoizable = False
        self.assertFalse(mod0.is_memoizable())


    def test_turn_off_memoization(self):
        mod = pp.Module()
        self.assertRaises(RuntimeError, mod.turn_off_memoization)

        mod0 = self.nondefault_mod
        mod0.turn_off_memoization()
        self.assertFalse(mod0._is_memoizable)

        # Calling it twice does nothing
        mod0.turn_off_memoization()
        self.assertFalse(mod0._is_memoizable)


    def test_turn_on_memoization(self):
        mod = pp.Module()
        self.assertRaises(RuntimeError, mod.turn_on_memoization)

        # Does nothing if already memoizable
        mod0 = self.nondefault_mod
        self.assertTrue(mod0._is_memoizable)
        mod0.turn_on_memoization()
        self.assertTrue(mod0._is_memoizable)

        # Actually turns it on, if it was off
        mod0._is_memoizable = False
        mod0.turn_on_memoization()
        self.assertTrue(mod0._is_memoizable)


    def test_lock(self):
        # Raises an error if no callback
        mod = pp.Module()
        self.assertRaises(RuntimeError, mod.lock)

        # Raises an error if a submodule isn't ready
        mod0 = self.nondefault_mod
        self.assertRaises(RuntimeError, mod0.lock)

        # Can lock a ready module
        self.ready_submod.lock()
        self.assertTrue(self.ready_submod.locked())


    def test_results(self):
        mod = pp.Module()
        self.assertRaises(RuntimeError, mod.results)

        mod1 = self.nondefault_mod
        corr = set(['result x', 'result 0'])
        self.assertEqual(mod1.results(), corr)


    def test_inputs(self):
        mod = pp.Module()
        self.assertRaises(RuntimeError, mod.results)

        mod0 = self.nondefault_mod
        corr = {'input 0' : None, 'input x' : None }
        self.assertEqual(mod0.inputs(), corr)


    def test_submods(self):
        mod = pp.Module()
        self.assertRaises(RuntimeError, mod.submods)

        mod0 = self.nondefault_mod
        corr = {'callback 0' : None}
        self.assertEqual(mod0.submods(), corr)

        mod0._state['submods'][('callback 0', PT0())] = self.ready_submod
        corr = {'callback 0' : self.ready_submod}
        self.assertEqual(mod0.submods(), corr)


    def test_property_types(self):
        mod = pp.Module()
        self.assertRaises(RuntimeError, mod.property_types)

        mod0 = self.nondefault_mod
        corr = set([PT0()])
        self.assertEqual(mod0.property_types(), corr)


    def test_description(self):
        # Raises an error if no callback
        mod = pp.Module()
        self.assertRaises(RuntimeError, mod.description)

        # Raises an error if no description
        mod0 = self.ready_submod
        self.assertRaises(RuntimeError, mod0.description)

        mod0._state['description'] = 'hello world'
        self.assertEqual(mod0.description(), 'hello world')


    def test_citations(self):
        # Raises an error if no callback
        mod = pp.Module()
        self.assertRaises(RuntimeError, mod.citations)

        # No citations
        mod0 = self.ready_submod
        self.assertEqual(mod0.citations(), [])

        # Citations
        mod1 = self.nondefault_mod
        self.assertEqual(mod1.citations(), ['foo et al.'])


    def test_change_input(self):
        # Raises an error if no callback
        mod = pp.Module()
        self.assertRaises(RuntimeError, mod.change_input, 'input 0', 42)

        # Raises an error if the module is locked
        mod0 = self.ready_submod
        mod0.lock()
        self.assertRaises(RuntimeError, mod0.change_input, 'input 0', 99)

        # Can actually change the input
        mod1 = self.nondefault_mod
        mod1.change_input('input x', 42)
        corr = {'input 0' : None, 'input x' : 42}
        self.assertEqual(mod1.inputs(), corr)

        # Raises an error if the key does not exist
        self.assertRaises(KeyError, mod1.change_input, 'not a key', 42)


    def test_change_submod(self):
        # Raises an error if no callback
        mod = pp.Module()
        self.assertRaises(RuntimeError, mod.change_submod, 'callback 0', None)

        # Raises an error if the module is locked
        mod0 = self.ready_submod
        mod0.lock()
        self.assertRaises(RuntimeError, mod0.change_submod, 'input 0', 99)

        # Can actually change the input
        mod1 = self.nondefault_mod
        mod1.change_submod('callback 0', mod0)
        corr = {'callback 0' : mod0}
        self.assertEqual(mod1.submods(), corr)

        # Raises an error if the key does not exist
        self.assertRaises(KeyError, mod1.change_submod, 'not a key', mod0)

    def test_run_as(self):
        pt = PT0()

        # Raises an error if no callback
        mod = pp.Module()
        self.assertRaises(RuntimeError, mod.run_as, pt, 42)

        # Can run a ready Module
        mod0 = self.ready_submod
        self.assertEqual(mod0.run_as(pt, 42), 42)

        # Raises an error if not ready
        mod1 = self.not_ready_submod
        self.assertRaises(RuntimeError, mod1.run_as, pt, 42)

        # Raises an error if it does not satisfy the property type
        mod0._state['property_types'] = set()
        self.assertRaises(RuntimeError, mod0.run_as, pt, 42)


    def test_run(self):
        inputs = {'input 0' : 42}
        corr = {'result 0' : 42}

        # Raises an error if no callback
        mod = pp.Module()
        self.assertRaises(RuntimeError, mod.run, inputs)

        # Can run a ready Module
        mod0 = self.ready_submod
        self.assertEqual(mod0.run(inputs), corr)

        # Raises an error if not ready
        mod1 = self.not_ready_submod
        self.assertRaises(RuntimeError, mod1.run, inputs)


    def test_comparisons(self):
        lhs, rhs = pp.Module(), pp.Module()

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

        lhs._state['results'] = set(['hello'])
        rhs._state['results'] = set(['bar'])
        self.assertNotEqual(lhs, rhs)
        lhs._state['results'] = set(['bar'])
        self.assertEqual(lhs, rhs)

        lhs._state['inputs']['hello'] = 'bar'
        rhs._state['inputs']['hello'] = 'world'
        self.assertNotEqual(lhs, rhs)
        lhs._state['inputs']['hello'] = 'world'
        self.assertEqual(lhs, rhs)

        # TODO: Test Submods

        # TODO: Test property types

        lhs._state['citations'] = set(['Foo et al.'])
        rhs._state['citations'] = set(['Bar et al.'])
        self.assertNotEqual(lhs, rhs)
        lhs._state['citations'] = set(['Bar et al.'])
        self.assertEqual(lhs, rhs)
