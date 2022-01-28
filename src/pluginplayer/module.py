from copy import deepcopy
from re import L


class Module:
    """ Encapsulates a user-supplied function.

    To extend the functionality of a program written on top of PluginPlay, users
    write modules. Each Module instance is essentially a function with some
    associated meta-data. In the real PluginPlay Module creation is rather
    involved. Here we focus on the main aspects of the Module class:

    #. It's API (the API presented here closesly mirrors the real API)
    #. It has some state injected by PluginPlay (e.g., ``_locked``, and
       ``_is_memoizable``)
    #. It has state set by the Module developer (``_state``)
    #. It wraps some underlying callback
    #. Manipulation of most of the Module's state is done through the
       ModuleManager

    Keep in mind the real implementation is written in C++ and exposed to
    Python, whereas this implementation here is simply meant to provide a
    working implementation of the real API. The point being the API and design
    of this class may seem heavy-handed and odd at times, but in the real class
    there's (usually) reasons for the design.
    """

    def __init__(self, **kwargs):
        r""" Creates a Module instance initialized with the provided state

        In practice Modules are initialized by the library which provides them.
        This initialization process can be rather complex. For the purposes of
        the PluginPlay API we just specify this state via the ctor.

        :param \**kwargs: See below

        :Keyword Arguments:
           - *callback_name* (``str``) -- A distinguishing name for the wrapped
             callback.
           - *callback* (``callable``) -- The actual callback to wrap.
           - *citations* (``[str]``) -- What sources users of this module should
             cite and/or give credit to.
           - *description* (``str``) -- A detailed description of what the
             callback does.
           - *inputs* (``{str : obj}``) -- Map from the name of the input to its
             default value for additional inputs recognized by the callable
             beyond those specified in the property types.
           - *property_types* (``{PropertyTypes}``) -- Set of property types
             that the callback can be used as.
           - *results* (``{str}``) -- Set containing the names of the additional
             results the callback returns beyond those of the property types.
           - *submods* (``{str : Module}``) -- Map from callback point to the
             callback which should be called at that point.
        """

        # Tracks whether the module is unlocked (meaning user can modify)
        self._unlocked = True

        # Used to memoize calls to the module
        self._cache = {}

        # Flag indicating whether memoization is possible
        self._is_memoizable = True

        # In the real PluginPlay this is a class wrapping the user's class.
        # Here we just put the main pieces of that class's state into a dict
        self._state = {'callback_name' : None,
                       'callback' : None,
                       'citations' : [],
                       'description' : None,
                       'inputs' : {},
                       'property_types' : set(),
                       'results' : set(),
                       'submods' : {},
                       }

        # Parse the kwargs
        for k in self._state.keys():
            if k in kwargs:
                self._state[k] = kwargs[k]


    def unlocked_copy(self):
        """Makes a deepcopy of the current module, which can be modified.

        Once a Module instance starts running its state can no longer be
        modified. Sometimes a user wants to run the same instance again, but
        with slightly different state. This function can be used to create a
        deep copy (*i.e.*, not aliased to the present instance) which can be
        modified.

        :return: A deepcopy of the current instance, except that the copy is
                 unlocked.
        :rtype: Module
        """
        rv = deepcopy(self)
        rv._unlocked = True
        return rv

    def has_module(self):
        """Determines if the current Module actually wraps a callable.

        For various reasons we need the Module class to be default constructable
        (*i.e.*, constructor can be called with no arguments). If an instance is
        default constructed then it won't contain a callback. This function can
        be used to check if the present instance contains a callback or not.

        :return: True if this instance wraps a callback and False otherwise.
        :rtype: bool
        """

        return self._state['callback'] != None

    def has_description(self):
        """Determines if a module has a description.

        For the PluginPlay Mokup this function is fairly trivial. In the real
        PluginPlay there are several levels of indirection which make this less
        obvious.

        :return: True if this instance has a description and False otherwise.
        :rtype: bool
        """

        return self._state['description'] != None

    def locked(self):
        """If a Module is locked, users can no longer modify its state.

        Modules may be run concurrently. Before the Module is run it is first
        locked. Once a Module is locked its state can no longer be changed and
        consequently we don't have to worry about its state being changed while
        it is running.

        :return: True if the module is locked and False otherwise.
        :rtype: bool
        """

        return not self._unlocked

    def list_not_ready(self):
        pass

    def ready(self, prop_type):
        """Determines if the present Module can be run as PropertyType prop_type

        :param prop_type: The PropertyType we are attempting to run the module
                          as.
        :type prop_type: PropertyType

        :return: True if in its current state the present instance can be run as
                 PropertyType prop_type and False otherwise.
        :rtype: bool
        """
        return True

    def reset_cache(self):
        """Forgets all the results that the Module has computed.

        For performance reasons and for reproducability reasons, Module
        instances keep track of all of the results they have computed. These
        results are stored in an internal cache. It is sometimes the case that
        these caches can fill up with large temporary intermediates. This
        function wipes out the cache associated with this Module.
        """

        self._cache = {}

    def is_memoizable(self):
        """Determines if calls to the Module can be memoized.

        Memoization is a technique where calls to functions are ellided when the
        results are already known. Typically this is done by storing a hash map
        from inputs to already computed results. That said, not all functions
        can be ellided (for example those which invoke random number generators,
        or those which use additional inputs beyond the ones which were hashed).
        Furthermore the user may not want a call to be memoized (e.g., if
        storing the result long term would consume too many resources).

        Regardless of the reason why it, or why it can not, this function is
        used to determine if calls to the current Module can be memoized.
        """
        return self._is_memoizable

    def turn_off_memoization(self):
        """Makes it so that the Module actually runs everytime it is called."""
        self._is_memoizable = False

    def turn_on_memoization(self):
        """When on the Module will avoid rerunning previously seen inputs."""
        self._is_memoizable = True

    def lock(self):
        """When a Module is locked its state can no longer be changed.

        Calling this function will lock the Module. Once locked all attempts to
        change the Module through the public API will raise exceptions.
        """
        self._unlocked = False

    def results(self):
        return self._state['results']

    def inputs(self):
        return self._state['inputs']

    def submods(self):
        return self._state['submods']

    def property_types(self):
        return self._state['property_types']

    def description(self):
        return self._state['description']

    def citations(self):
        return self._state['citations']

    def change_input(self, key, value):
        if key in self.inputs():
            self.inputs()[key] = value

        raise KeyError(key + " is not a valid input for this Module.")

    def change_submod(self, key, new_mod):
        if key in self.submods():
            self.submods()[key] = new_mod

        raise KeyError(key + " is not a predefined callback point.")

    def add_property_type(self, new_prop_type):
        self._property_types.append(new_prop_type)

    def run_as(prop_type, *args):
        pass

    def run(inputs):
        """This call actually runs the Module with the provided inputs.

        Each Module instance has some input state bound to it. In particular it
        has input parameter values bound to ``Module._state['inputs']`` and
        submodules bound to ``Module._state['submods']``. The actual call to the
        submodule is given ``Module._state['submods']`` and the union of
        ``inputs`` with ``Module._state['inputs']``.

        :param inputs: The positional arguments given to the Module, wrapped in
                       a dictionary.
        :type inputs: {str, obj}

        :return: A dictionary whose keys are the names of the results and whose
                 values are the values of the respective result.
        :rtype: {str, obj}
        """

        pass

    def hash(self):
        pass

    def __eq__(self, rhs):
        """Determines if the state of this instance is the same as that of rhs.

        Equality comparison considers locked state, callback properties (name,
        description, property types, and citations), bound inputs, bound
        submodules, and result keys. Not included are whether or not the module
        is going to be memoized and the value of its cache.

        :param rhs: The instance we are comparing against
        :type rhs: Module

        :return: True if this instance compares equal to rhs and False
                 otherwise.
        :rtype: bool
        """

        return self._unlocked == rhs._unlocked and self._state == rhs._state

    def __ne__(self, rhs):
        """Determines if this Module instance is different than rhs.

        Different, *i.e.*, not equal, is implemented by negating the value
        equal operation. Thus two Module instances are different if they are not
        equal.

        :param rhs: The instance we are comparing against.
        :type rhs:  Module

        :return: False if if this instance compares equal to rhs and True
                 otherwise.
        :rtype: bool
        """
        return not self == rhs

    def __repr__(self):
        return str('Unlocked : %s\n' % self._unlocked) + \
               str('State    : %s\n' % self._state)


def print_not_ready(mod, inputs, indent):
    pass
