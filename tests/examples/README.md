# examples Directory

This directory contains four things:

- `geometry` - An example module collection for computing geometric properties
  of shapes
- `__init__.py` - Makes this folder a Python module so that the Python
  `unittest` module will pick it up.
- `README.md` - The readme you are currently reading.
- `test_examples.py` - A curated example of interacting with the geometry
  modules through PluginPlay

The following subsections contain some additional details (regarding the
important ones).

## geometry

PluginPlay is just a framework for creating the call graph for a modular
program. By itself PluginPlay has none of the program's functionality.
Developers add functionality to PluginPlay by writing modules. Typically the
developers write more than one module and distribute their modules as a single
package (usually a C++ library). The package of modules is called a "module
collection".

The `geometry` directory contains an example module collection. It defines two
property types (i.e., ways to call a module):

- `Area` - for modules which can compute the area of a shape, and
- `PrismVolume` - for modules which can compute the volume of a prism

It also includes a series of modules:

- `Rectangle` - computes the area of a rectangle
- `Square` - computes the area of a square
- `Triangle` - computes the area of a triangle
- `PrismVolumeBySubmod` - computes the volume of a prism using a submodule to
  compute the area of the base.

Typical usage would be something like:

```.py
import geometry
import pluginplay as pp

mm = pp.ModuleManager()
geometry.load_modules(mm)

area = mm.run_as(geometry.Area(), "Area of a triangle", 1.2, 3.4)
```

See the `test_examples.py` script for a more detailed example (albeit with
unit testing cluttering the presentation).
