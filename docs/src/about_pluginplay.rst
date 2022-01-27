About PluginPlay
================

The point of this page is to give a brief high-level overview of the PluginPlay
framework. Subsequent sections will give code examples.

PluginPlay is a software framework used by C++ program developers wanting to
write extremely flexible software packages. In particular packages built on
PluginPlay can:

- have their call graph inspected, reordered, and dynamically extended;
- be extended with new functionality via plugins;
- dynamically add new plugin communication protocols;
- and be driven entirely from Python

When interacting with a package built on top of PluginPlay users interact
primarily with two classes ``ModuleManager`` and ``Module``. Each ``Module``
instance encapsulates a specific piece of functionality. The list of ``Module``
instances presently known to the program is stored in the ``ModuleManager``.
Users add new functionality to the program by registering new ``Module``
instances with the ``ModuleManager``. The ``ModuleManager`` then facilitates
propagating the new module throughout the call graph. When a user is satisfies
with the current call graph, they ask the ``ModuleManager`` instance for the
``Module`` they would like to run and then run it, PluginPlay does the rest.

Ultimately each ``Module`` instance takes as input two dictionaries. The first
dictionary defines a list of input parameters (the key is the name of the
parameter and the value is the value of the parameter). The second dictionary
contains callbacks that the body of the ``Module`` should use (the keys are
the names of the predefined callback points, and the values are ``Module``
instances to call). The result of calling a ``Module`` is also a dictionary
(keys are the names of each result, and the values are the value of the result).

As was just described all ``Module`` instances have the same API as far as
typing goes; however, the dictionary keys each ``Module`` instance recognizes
will in general vary from instance to instance. In order to know how each
``Module`` should be used PluginPlay defines a concept known as a "property
type", which is codified by the ``PropertyType`` class. Essentially a property
type is a communication protocol defining a specific set of input parameters
and a specific set of results. In the process of registering a ``Module``
instance ``mod`` with a ``ModuleManager`` instance ``mm``, ``mm`` is told:

- what property types ``mod`` can be run as,
- the names of the callback points inside ``mod``, and
- the property types of each callback point inside ``mod``

With this information the ``mm`` knows where ``mod`` can be deployed in the call
graph, as well as what deployment points ``mod`` itself contains.
