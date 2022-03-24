class PropertyType:
    """Defines an effective function API for calling a Module.

    All Module instances actually are invoked like:

    .. code-block:: py

       mod = module.Module()
       results = mod.run(inputs)

    where both results and inputs are kwargs-like.

    Particluarly in C++ the wrapping and unwrapping of the the inputs and
    results is a lot of nasty, heavily templated boilerplate. For this reason we
    came up with the "property type" concept. Each property type defines a
    mapping from positional arguments to their elements in the inputs/results
    maps passed to ``Module.run``. Using the property type ``PT`` a call to run
    a ``Module`` looks more like:

    .. code-block:: py

       result0, result1, result2 = module.run_as(PT, input0, input1)


    Users are expected to use the PropertyType class by inheriting from it. Then
    in the ctor of the derived class they should set the inputs and results
    members. For example to implement the class for ``PT`` above:

    .. code-block:: py

        class PTClass(property_type.PropertyType):

            def __init__(self):
                inputs = [('input0', None), ('input1', None)]
                results = ['result0', 'result1', 'result2']
                return super().__init__(inputs, results)

    If applicable the ``None`` values could be replaced with default values.
    """

    def __init__(self, inputs = [], results = []):
        """Simply sets the state to the provided inputs and results."""

        # A list of pairs, 0-th element is name, 1-st is defaul value
        self._inputs = inputs

        # A list of result names
        self._results = results


    def inputs(self):
        """Returns the inputs that the derived class set.

        The real implementation of PropertyType is significantly more
        complicated than simply having the derived class set the base class's
        state. The ``inputs`` function wraps the gymnastics required to get the
        input parameters set by the derived class.

        :return: The inputs which were set by the derived class. Each input is a
                 pair such that the 0-th element is the description/name of the
                 parameter and the 1-st element is the default value of the
                 parameter.
        :rtype: list(set(str, obj))
        """
        return self._inputs


    def results(self):
        """Returns the results that the derived class set.

        The real implementation of PropertyType is significantly more
        complicated than simply having the derived class set the base class's
        state. The ``results`` function wraps the gymnastics required to get the
        results set by the derived class.

        :return: The results which were set by the derived class. Results do not
                 have default values so their only state is the name of the
                 result.
        :rtype: list(str)
        """
        return self._results


    def wrap_inputs(self, inputs, *args):
        """Merges the positional arguments args into the provided set of inputs.

        The derived class established a mapping from positional input arguments
        to keys. This function uses that mapping to insert ``args`` into the
        provided dictionary. After this call, ``args`` will have been inserted
        into ``inputs``. Any keys in ``inputs`` which are not keys for this
        property type will be left alone; however, keys which are names of
        input parameters known to this property type will have their values
        overridden.


        :param inputs: The dictionary we are inserting ``args`` in to. Will be
                       modified as a result of calling this function.
        :type inputs: dict(str, obj)


        :param \*args: A variadic set of values which are treated as positional
                       arguments to a function. The number of arguments must
                       minimally equal the number of inputs without default
                       values and can not exceed the number of recognized
                       inputs.


        :raises RuntimeError: If the user passes more arguments than the derived
                              class set.

        :raises RuntimeError: If the user does not set a value for all
                              positional arguments without default values.
        """
        max_nargs = len(self.inputs())
        if len(args) > max_nargs:
            raise RuntimeError("Expected at most %s arguments." % max_nargs)

        # We were provided arguments for the first len(args) positional args
        for i in range(len(args)):
            inputs[self._inputs[i][0]] = args[i]

        # Remaining max_nargs - len(args) args are default initialized
        for i in range(len(args), max_nargs):
            k, v = self._inputs[i]
            if v == None:
                raise RuntimeError('No default argument for ' + k)

            inputs[k] = v


    def wrap_results(self, results, *args):
        """Merges the positional arguments args into the provided results.

        The derived class established a mapping from positional results
        to keys. This function uses that mapping to insert ``args`` into the
        provided dictionary. After this call, ``args`` will have been inserted
        into ``results``. Any keys in ``results`` which are not keys for this
        property type will be left alone; however, keys which are names of
        input parameters known to this property type will have their values
        overridden.


        :param results: The dictionary we are inserting ``args`` in to. Will be
                        modified as a result of calling this function.
        :type results: dict(str, obj)


        :param \*args: A variadic set of values which are treated as positional
                       returns from a function. The number of arguments must
                       equal the number of results set by the derived class.


        :raises RuntimeError: If the user passes a different number of results
                              than the derived class defined.
        """
        max_nargs = len(self._results)
        if len(args) != max_nargs:
            raise RuntimeError("Expected exactly %s argument(s)" % max_nargs)

        for k, v in zip(self._results, args):
            results[k] = v


    def unwrap_inputs(self, inputs):
        """Converts from key-value pairs to positional arguments.

        The derived class defines a mapping from positional input arguments to
        keys. This function reverse that mapping to pull arguments out of an
        associative array. This is useful for implementing the callback of a
        Module.

        :param inputs: A map from input name/descriptions to values.
        :type inputs: map(str, obj)

        :return: The inputs known to this property type, in the order they were
                 declared.
        :rtype: For a single input the return of this function is just the value
                if there are multiple returns it is a list of values.

        :raises KeyError: If one of the inputs known to this property type is
                          not in ``inputs``.
        """
        rv = []
        for k, _ in self._inputs:
            if k not in inputs:
                raise KeyError(k + " is not in the inputs to parse.")
            rv.append(inputs[k])
        if len(rv) == 1:
            return rv[0]
        return rv


    def unwrap_results(self, results):
        """Converts from key-value pairs to positional returns.

        The derived class defines a mapping from positional returns to
        keys. This function reverse that mapping to pull the results out of an
        associative array.

        :param inputs: A map from result name/descriptions to values.
        :type inputs: map(str, obj)

        :return: The results known to this property type, in the order they were
                 declared.
        :rtype: For a single input the return of this function is just the value
                if there are multiple returns it is a list of values.

        :raises KeyError: If one of the results known to this property type is
                          not in ``results``.
        """
        rv = []
        for k in self._results:
            if not k in results:
                raise KeyError(k + " is not in the results to parse.")
            rv.append(results[k])
        if len(rv) == 1:
            return rv[0]
        return rv


    def __eq__(self, rhs):
        """Determines if two PropertyTypes are equivalent.

        For the purposes of this mock up, two PropertyType instances are equal
        if they define the same set of inputs (with the same default values) and
        the same set of results. In practice the real comparison is polymorphic
        and also requires that the derived classes have the same type.

        :param rhs: The instance we are comparing to.
        :type rhs: PropertyType

        :return: True if this instance compares equal to ``rhs`` and False
                 otherwise.
        :rtype: bool
        """
        return self._inputs == rhs._inputs and self._results == rhs._results

    def __hash__(self):
        return hash((tuple(self._inputs), tuple(self._results)))
