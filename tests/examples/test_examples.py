from . import geometry
import unittest
import pluginplay as pp

# The first thing a user of PluginPlay does is import the plugins they want to
# use (here that's the module collection in the provided geometry package), then
# they import pluginplay

class TestExamples(unittest.TestCase):

    def setUp(self) -> None:
        # After the initial imports users create a ModuleManager instance
        self.mm = pp.ModuleManager()

        # and then populate it (there can be a number of load_module calls
        # depending on how many module collections they want to load)
        geometry.load_modules(self.mm)


    def test_area(self):
        # This example is the most straightforward use of PluginPlay.
        #
        # With an initialized ModuleManager, we select the module we want to
        # run, and run it:

        area = self.mm.run_as(geometry.Area(), "Area of a triangle", 1.2, 3.4)

        # Explanation:
        #
        # All modules actually have an API which takes a set of kwargs and
        # returns a set of kwargs. The above call puts a nicer API over top of
        # that by saying we want to run the module as a module which can compute
        # an ``Area```. What it means to be able to compute an ``Area`` is
        # defined by the ``geometry.Area`` class. Specifically it specifies that
        # a module should take two positional inputs: the base of the shape and
        # the height of the shape and return a single result, the area.
        #
        # The remaining arguments are:
        #
        # - ``"Area of a triangle"`` which is the identifier of the module we
        #   want to run.
        # - ``1.2`` which is the first positional argument to pass to the
        #   module
        # - ``3.4`` which is the second positional argument to pass
        #
        # The meaning of the arguments is defined in the ``geometry.Area()``
        # class.

        self.assertEqual(area, 0.5 * 1.2 * 3.4)

        # Runing the other area modules is done similarly

        area = self.mm.run_as(geometry.Area(), "Area of a square", 1.2, 1.2)
        self.assertEqual(area, 1.2 * 1.2)

        area = self.mm.run_as(geometry.Area(), "Area of a rectangle", 1.2, 3.4)
        self.assertEqual(area, 1.2 * 3.4)


    def test_volume(self):
        # This test demonstrates using a module that has a submodule. In this
        # case we use the PrismVolume module. This module computes the volume of
        # a prism by computing the area of the base and multiplying it by the
        # height of the prism. The formula for the area of the base varies
        # depending on the shape of the base, so the volume module defers to a
        # submodule for the area of base.

        # We start by showing how we could compute the area of a cube. For a
        # cube the base is a square, so we change the prism module's area
        # submodule to the module for computing the area of a square
        mod_key = 'Volume of a prism'
        self.mm.change_submod(mod_key, 'area', 'Area of a square')

        # Now the prism module can be run analogously to the last test
        vol = self.mm.run_as(geometry.PrismVolume(), mod_key, 1.2, 1.2, 1.2)
        self.assertEqual(vol, 1.2 * 1.2 * 1.2)


        # What if we wanted to compute the volume of a triangluar prism?
        # We can't just change the 'area' submodule of 'Volume of a prism'
        # because the module has since been locked. Feel free to uncomment the
        # following line to prove that to yourself:
        #
        # self.mm.change_submod(mod_key, 'area', 'Area of a triangle')
        #
        # So instead we first copy the 'Volume of a prism' module:
        mod0_key = 'Triangular prism'
        self.mm.copy_module(mod_key, mod0_key)
        self.mm.change_submod(mod0_key, 'area', 'Area of a triangle')

        # and then run the now setup module
        vol = self.mm.run_as(geometry.PrismVolume(), mod0_key, 1.2, 2.3, 3.4)
        self.assertEqual(vol, 0.5 * 1.2 * 2.3 * 3.4)
