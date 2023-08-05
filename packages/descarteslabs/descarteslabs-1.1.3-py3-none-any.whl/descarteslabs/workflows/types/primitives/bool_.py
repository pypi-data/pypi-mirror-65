from ...cereal import serializable
from ..core import allow_reflect
from .primitive import Primitive
from ..mixins import NumPyMixin


def _delayed_numpy_overrides():
    # avoid circular imports
    from descarteslabs.workflows.types.numpy import numpy_overrides

    return numpy_overrides


@serializable()
class Bool(NumPyMixin, Primitive):
    """
    Proxy boolean.

    Note that this cannot be compared with Python's ``and`` and ``or`` operators;
    you must use the bitwise operators ``&`` and ``|``. Also note that more parenthesis are needed
    with bitwise operators than with ``and`` and ``or``.

    Examples
    --------
    >>> from descarteslabs.workflows import Bool
    >>> my_bool = Bool(True)
    >>> my_bool
    <descarteslabs.workflows.types.primitives.bool_.Bool object at 0x...>
    >>> other_bool = Bool(False)
    >>> val = my_bool | other_bool
    >>> val.compute() # doctest: +SKIP
    True
    """

    _pytype = bool

    def __bool__(self):
        raise TypeError(
            "Workflows objects cannot be used in conditionals.\n\n"
            "Your code (or code you're calling) is trying to use a Workflows "
            "{} object to make an immediate yes/no decision. This isn't possible, "
            "because we don't know if the value is True or False without calling `compute`.\n\n"
            "Depending on what you're trying to do, here are some ways to refactor your code:\n"
            " - Use bitwise operators (like & and |)\n"
            " - In place of `y in x` use `y.contains(x)` ('y' must be a proxy object so use "
            "`wf.proxify(y)` if it's a Python list or dict)\n"
            " - There is currently no direct Workflows equivalent to `if x` but you "
            "can construct a `Dict` from `x -> y` and select values out of it with "
            "'x' or use `wf.where` to achieve a similar result.".format(
                type(self).__name__
            )
        )

    def __invert__(self):
        return _delayed_numpy_overrides().logical_not(self)

    @allow_reflect
    def __eq__(self, other):
        return _delayed_numpy_overrides().equal(self, other)

    @allow_reflect
    def __ne__(self, other):
        return _delayed_numpy_overrides().not_equal(self, other)

    @allow_reflect
    def __and__(self, other):
        return _delayed_numpy_overrides().logical_and(self, other)

    @allow_reflect
    def __or__(self, other):
        return _delayed_numpy_overrides().logical_or(self, other)

    @allow_reflect
    def __xor__(self, other):
        return _delayed_numpy_overrides().logical_xor(self, other)

    @allow_reflect
    def __rand__(self, other):
        return _delayed_numpy_overrides().logical_and(other, self)

    @allow_reflect
    def __ror__(self, other):
        return _delayed_numpy_overrides().logical_or(other, self)

    @allow_reflect
    def __rxor__(self, other):
        return _delayed_numpy_overrides().logical_xor(other, self)
