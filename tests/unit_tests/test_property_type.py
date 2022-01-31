from pluginplay import property_type
import unittest

# Define some example property types for unit testing purposes
class PT0(property_type.PropertyType):
    """Effective signature: result0 (input0)"""

    def __init__(self):
        inputs = [('input 0', None)]
        results = ['result 0']
        return super().__init__(inputs, results)


class PT1(property_type.PropertyType):
    """Effective signature: result0 (input0, input1 = 42)"""

    def __init__(self):
        inputs = [('input 0', None), ('input 1', 42)]
        results = ['result 0']
        return super().__init__(inputs, results)


class PT2(property_type.PropertyType):
    """Effective signature: result0, result 1 (input0, input1 = 42)"""

    def __init__(self):
        inputs = [('input 0', None), ('input 1', 42)]
        results = ['result 0', 'result 1']
        return super().__init__(inputs, results)


class TestPropertyType(unittest.TestCase):

    def test_ctor(self):
        pt0 = PT0()
        self.assertEqual(pt0._inputs, [('input 0', None)])
        self.assertEqual(pt0._results, ['result 0'])

        pt1 = PT1()
        self.assertEqual(pt1._inputs, [('input 0', None), ('input 1', 42)])
        self.assertEqual(pt1._results, ['result 0'])

        pt2 = PT2()
        self.assertEqual(pt2._inputs, [('input 0', None), ('input 1', 42)])
        self.assertEqual(pt2._results, ['result 0', 'result 1'])


    def test_inputs(self):
        pt0 = PT0()
        self.assertEqual(pt0.inputs(), [('input 0', None)])

        pt1 = PT1()
        self.assertEqual(pt1.inputs(), [('input 0', None), ('input 1', 42)])

        pt2 = PT2()
        self.assertEqual(pt2.inputs(), [('input 0', None), ('input 1', 42)])


    def test_results(self):
        pt0 = PT0()
        self.assertEqual(pt0.results(), ['result 0'])

        pt1 = PT1()
        self.assertEqual(pt1.results(), ['result 0'])

        pt2 = PT2()
        self.assertEqual(pt2.results(), ['result 0', 'result 1'])


    def test_wrap_inputs(self):
        pt0 = PT0()
        inputs = {}
        pt0.wrap_inputs(inputs, 2)
        self.assertEqual(inputs, {'input 0' : 2})

        # Checks that it overwrites existing value and can insert default value
        pt1 = PT1()
        inputs = {'input 0' : 10}
        pt1.wrap_inputs(inputs, 2)
        self.assertEqual(inputs, {'input 0' : 2, 'input 1' : 42})

        # Checks that it leaves unrecognized inputs alone
        pt2 = PT2()
        inputs = {'hello' : 'world'}
        pt2.wrap_inputs(inputs, 2, 10)
        self.assertEqual(inputs, {'input 0' : 2,
                                  'input 1' : 10,
                                  'hello' : 'world'})

        # Raises an error if it gets too many arguments
        inputs = {}
        self.assertRaises(RuntimeError, pt0.wrap_inputs, inputs, 2, 3)

        # Error if there isn't a default argument for unspecified parameters
        inputs = {}
        self.assertRaises(RuntimeError, pt0.wrap_inputs, inputs)


    def test_wrap_results(self):
        pt0 = PT0()
        results = {}
        pt0.wrap_results(results, 3)
        self.assertEqual(results, {'result 0' : 3})

        # Overrides existing result
        pt1 = PT1()
        pt1.wrap_results(results, 42)
        self.assertEqual(results, {'result 0' : 42})

        # Multiple resutls and ignores existing results
        pt2 = PT2()
        results = {'result a' : 9}
        pt2.wrap_results(results, 2, 42)
        self.assertEqual(results, {'result 0' : 2,
                                   'result 1' : 42,
                                   'result a' : 9})

        # Raises an error if we provide too many arguments
        self.assertRaises(RuntimeError, pt0.wrap_results, results, 1, 2)

        # Raises an error if we provide too few arguments
        self.assertRaises(RuntimeError, pt0.wrap_results, results)


    def test_unwrap_inputs(self):

        inputs = {'input 0' : 0, 'input 1' : 1, 'input 2' : 2}

        pt0 = PT0()
        self.assertEqual(pt0.unwrap_inputs(inputs), 0)

        # Typically used like this
        pt1 = PT1()
        r0, r1 = pt1.unwrap_inputs(inputs)
        self.assertEqual(r0, 0)
        self.assertEqual(r1, 1)

        pt2 = PT2()
        self.assertEqual(pt2.unwrap_inputs(inputs), [0, 1])

        # Raises an error if a key is not in the inputs
        self.assertRaises(KeyError, pt0.unwrap_inputs, {})

    def test_unwrap_results(self):

        inputs = {'result 0' : 0, 'result 1' : 1, 'result 2' : 2}

        pt0 = PT0()
        self.assertEqual(pt0.unwrap_results(inputs), 0)

        pt1 = PT1()
        self.assertEqual(pt1.unwrap_results(inputs), 0)

        # Typically used like this
        pt2 = PT2()
        r0, r1 = pt2.unwrap_results(inputs)
        self.assertEqual(r0, 0)
        self.assertEqual(r1, 1)

        # Raises an error if a key is not in the inputs
        self.assertRaises(KeyError, pt0.unwrap_results, {})

    def test_comparisons(self):
        pt0 = PT0()
        self.assertEqual(pt0, PT0())

        #Different initial value
        diff_default = PT0()
        diff_default._inputs[0] = ('input 0', 42)
        self.assertNotEqual(pt0, diff_default)

        # Different inputs
        pt1 = PT1()
        self.assertNotEqual(pt0, pt1)

        # Different results
        pt2 = PT2()
        self.assertNotEqual(pt1, pt2)
