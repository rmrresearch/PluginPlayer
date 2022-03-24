from copy import deepcopy
class ModuleManager:
    """Manages the Module instances known to PluginPlay.

    The goal of the ModuleManager is to make it easier for users to interact
    with the call graph. To this end, each node is assigned a unique label
    called its "module key". Instead of specifiying a path through the call
    graph many operations can then be done by referring to a node by its key.
    """

    def __assert_has_key(self, key):
        """Code factorization for asserting that there is a module registered
            under the key ``key``.

        :raises KeyError: If there is no module stored under ``key``.
        """

        if key not in self._modules.keys():
            raise KeyError("ModuleManager does not have a module: %s." % key)


    def __assert_key_is_free(self, key):
        """Code factorization for asserting that a key is not in use.

        Keys need to be unique to avoid ambiguity when referring to nodes. This
        function checks that the provided input key is not already in use.

        :raises KeyError: If ``key`` is already assigned to a module.
        """

        if key in self._modules.keys():
            raise KeyError('Module key: %s is already in use.' % key)


    def __init__(self):
        """Creates a new, empty ModuleManager.

        For the purposes of this mock-up each ModuleManager is just a thin
        wrapper around a dictionary. The real ModuleManager is also charged with
        managing some additional runtime aspects, which we ignore.
        """
        self._modules = {}

    def __contains__(self, key):
        """Determines if there is a module registered under a key.

        :param key: The module key we are looking for.
        :type key: str

        :return: True if this instance contains a Module registered under
                 ``key`` and False otherwise.
        :rtype: bool
        """

        return key in self._modules.keys()


    def add_module(self, key, mod):
        """Registers a Module instance under the provided key.

        The ModuleManager is basically a dictionary from module keys to modules.
        This function registers a new module with the ModuleManager.

        :param key: The name to store the module under.
        :type key: str
        :param mod: The module we are registering with this ModuleManager.
        :type mod: Module

        :raises KeyError: If ``key`` is already in use.
        """

        self.__assert_key_is_free(key)
        self._modules[key] = mod


    def __getitem__(self, key):
        """Retrieves the module stored under ``key``.

        To interact with a Module users need to be able to get them back from
        the ModuleManager. That's what this function is for.

        :param key: The key for the requested module.
        :type key: str

        :return: The requested module.
        :rtype: Module

        :raises KeyError: If no module is registered under ``key``.
        """

        self.__assert_has_key(key)
        return self._modules[key]

    def copy_module(self, old_key, new_key):
        """Deep copies the specified module.

        If two different callback points are set to the same module key they
        will alias eachother (chaning the inputs or submods for one, will also
        change them for the other). Sometimes we don't want that. This function
        will create a deep copy of a module breaking the aliasing. The resulting
        module will be unlocked, allowing the user to change the inputs.

        :param old_key: The key of the module being deep copied.
        :type old_key: str
        :param new_key: The key to store the copy under.
        :type new_key: str

        :raises KeyError: If there is no module under ``old_key``
        :raises KeyError: If there is already a module under ``new_key``
        """

        self.__assert_has_key(old_key)
        self.__assert_key_is_free(new_key)
        self._modules[new_key] = self._modules[old_key].unlocked_copy()


    def erase(self, key):
        """Removes the specified module from the ModuleManager.

        After calling this function no module will be stored under ``key``.
        Note that if ``key`` is assigned as a submodule already this call will
        not unassign it.

        :param key: The key of the module being removed.
        :type key: str
        """
        if key in self._modules.keys():
            del self._modules[key]


    def rename_module(self, old_key, new_key):
        """Changes the key of a module.

        This function can be used to store a Module under a different key. After
        this call the Module will no longer be stored under the original key,
        leaving it free for use again.

        :param old_key: The key we are moving from.
        :type old_key: str
        :param new_key: The key we are moving to.
        :type new_key: str

        :raises KeyError: If there is no Module under ``old_key``
        :raises KeyError: If there is already a Module under ``new_key``.
        """

        self.copy_module(old_key, new_key)
        self.erase(old_key)


    def change_input(self, mod_key, opt_key, value):
        """Wraps the process of changing a Module's input value.

        This function makes it easier to change the input of a module directly
        through the ModuleManager. It ultimately just wraps getting the module
        and then calling ``change_input`` on the Module.

        :param mod_key: The key of the Module whose input is being changed.
        :type mod_key: str
        :param opt_key: The key of the option whose value is being changed.
        :type opt_key: str
        :param value: What the input should be changed to.

        :raises KeyError: If there is no Module under ``mod_key``.
        :raises KeyError: If there is no input under ``opt_key``.
        """
        self.__assert_has_key(mod_key)
        self._modules[mod_key].change_input(opt_key, value)


    def change_submod(self, mod_key, callback_key, submod_key):
        """Changes the submodule a Module calls.

        Modules define callback points. Users can change which modules are
        called at those callback points by using this function. Unlike going
        directly through the Module, using the ModuleManager to swap out
        submodules can be done purely with keys.

        :param mod_key: The key for the module whose submodule will be changed.
        :type mod_key: str
        :param callback_key: The identifier for the callback point to change.
        :type callback_key: str
        :param submod_key: The key of the module which should be called at the
                           callback point.
        :type submod_key: str

        :raises KeyError: If ``mod_key`` is not a valid module key.
        :raises KeyError: If ``callback_key`` is not a valid callback point
        :raises KeyError: If ``submod_key`` is not a valid module key.
        """

        self.__assert_has_key(mod_key)
        self.__assert_has_key(submod_key)
        new_submod = self._modules[submod_key]
        self._modules[mod_key].change_submod(callback_key, new_submod)

    def run_as(self, prop_type, mod_key, *args):
        """Runs a module as the specified properyt type.

        This function is a convenience function for grabbing a module and
        calling its ``run_as`` member.

        :param prop_type: The PropertyType defining how the module should be
                          run.
        :type prop_type: PropertyType
        :param mod_key: The key for the module to be run.
        :type mod_key: str
        :param \*args: The positional arguments the ``prop_type`` calls for.

        :return: The results defined by ``prop_type``.

        :raises KeyError: If ``mod_key`` is not a valid key.
        """
        self.__assert_has_key(mod_key)
        return self._modules[mod_key].run_as(prop_type, *args)
