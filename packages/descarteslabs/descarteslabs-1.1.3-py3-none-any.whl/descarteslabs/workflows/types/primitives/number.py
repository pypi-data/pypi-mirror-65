from ...cereal import serializable
from ..core import ProxyTypeError, typecheck_promote, allow_reflect
from ..mixins import NumPyMixin
from .bool_ import Bool
from .primitive import Primitive


def _delayed_numpy_overrides():
    # avoid circular imports
    from descarteslabs.workflows.types.numpy import numpy_overrides

    return numpy_overrides


def _binop_result(a, b):
    return Float if isinstance(a, Float) or isinstance(b, Float) else Int


@serializable()
class Number(NumPyMixin, Primitive):
    """
    Abstract base class for numeric Proxytypes.

    Use the concrete subtypes `Int` and `Float` instead;
    `Number` cannot be instantiated and should only be used for
    ``isinstance()`` checks.

    You can explicitly construct one numeric type from another,
    performing a cast (``Int(Float(4.2))``), but one numeric
    type will not implicitly promote to another (``Int._promote(Float(4.2))``
    will fail).
    """

    def __init__(self, obj):
        if isinstance(obj, Number) and not self._is_generic() or isinstance(obj, Bool):
            if isinstance(obj, type(self)):
                self.graft = obj.graft
            else:
                self.graft = self._from_apply(
                    "{}.cast".format(self.__class__.__name__), obj
                ).graft
        else:
            super(Number, self).__init__(obj)

    @classmethod
    def _promote(cls, obj):
        if isinstance(obj, cls):
            return obj
        elif isinstance(obj, Number):
            # Another Number that isn't our type:
            # we won't auto-convert it
            raise ProxyTypeError(
                "Cannot promote {} to {}. "
                "You need to convert it explicitly, like `{}(x)`".format(
                    type(obj), cls, cls.__name__
                )
            )
        else:
            return cls(obj)

    def __abs__(self):
        return _delayed_numpy_overrides().absolute(self)

    @allow_reflect
    def __add__(self, other):
        return _delayed_numpy_overrides().add(self, other)

    @allow_reflect
    def __div__(self, other):
        return _delayed_numpy_overrides().divide(self, other)

    @typecheck_promote(lambda: (Int, Float, Bool), _reflect=True)
    def __divmod__(self, other):
        from ..containers import Tuple

        restype = _binop_result(self, other)
        return Tuple[restype, restype]._from_apply("divmod", self, other)

    @allow_reflect
    def __eq__(self, other):
        return _delayed_numpy_overrides().equal(self, other)

    @allow_reflect
    def __floordiv__(self, other):
        return _delayed_numpy_overrides().floor_divide(self, other)

    def __hex__(self):
        raise TypeError(
            ("Cannot convert {} to Python string.").format(self.__class__.__name__)
        )

    @allow_reflect
    def __ge__(self, other):
        return _delayed_numpy_overrides().greater_equal(self, other)

    @allow_reflect
    def __gt__(self, other):
        return _delayed_numpy_overrides().greater(self, other)

    def __index__(self):
        raise TypeError(
            (
                "Cannot convert {} to Python int. A proxy type can "
                "only be used to slice other proxy types containers."
            ).format(self.__class__.__name__)
        )

    def __invert__(self):
        return self._from_apply("invert", self)

    @allow_reflect
    def __le__(self, other):
        return _delayed_numpy_overrides().less_equal(self, other)

    @allow_reflect
    def __lt__(self, other):
        return _delayed_numpy_overrides().less(self, other)

    @allow_reflect
    def __mod__(self, other):
        return _delayed_numpy_overrides().mod(self, other)

    @allow_reflect
    def __mul__(self, other):
        return _delayed_numpy_overrides().multiply(self, other)

    @allow_reflect
    def __ne__(self, other):
        return _delayed_numpy_overrides().not_equal(self, other)

    def __neg__(self):
        return _delayed_numpy_overrides().negative(self)

    def __pos__(self):
        return self._from_apply("pos", self)

    @allow_reflect
    def __pow__(self, other):
        return _delayed_numpy_overrides().power(self, other)

    @allow_reflect
    def __radd__(self, other):
        return _delayed_numpy_overrides().add(other, self)

    @allow_reflect
    def __rdiv__(self, other):
        return _delayed_numpy_overrides().divide(other, self)

    @typecheck_promote(lambda: (Int, Float, Bool))
    def __rdivmod__(self, other):
        from ..containers import Tuple

        restype = _binop_result(self, other)
        return Tuple[restype, restype]._from_apply("divmod", other, self)

    @allow_reflect
    def __rfloordiv__(self, other):
        return _delayed_numpy_overrides().floor_divide(other, self)

    @allow_reflect
    def __rmod__(self, other):
        return _delayed_numpy_overrides().mod(other, self)

    @allow_reflect
    def __rmul__(self, other):
        return _delayed_numpy_overrides().multiply(other, self)

    @allow_reflect
    def __rpow__(self, other):
        return _delayed_numpy_overrides().power(other, self)

    @allow_reflect
    def __rsub__(self, other):
        return _delayed_numpy_overrides().subtract(other, self)

    @allow_reflect
    def __rtruediv__(self, other):
        return _delayed_numpy_overrides().true_divide(other, self)

    @allow_reflect
    def __sub__(self, other):
        return _delayed_numpy_overrides().subtract(self, other)

    @allow_reflect
    def __truediv__(self, other):
        return _delayed_numpy_overrides().true_divide(self, other)


@serializable()
class Int(Number):
    """
    Proxy integer.

    Examples
    --------
    >>> from descarteslabs.workflows import Int
    >>> my_int = Int(2)
    >>> my_int
    <descarteslabs.workflows.types.primitives.number.Int object at 0x...>
    >>> other_int = Int(5)
    >>> val = my_int + other_int
    >>> val.compute() # doctest: +SKIP
    7
    >>> val = my_int < other_int
    >>> val.compute() # doctest: +SKIP
    True
    """

    _pytype = int

    @typecheck_promote(lambda: (Int, Bool), _reflect=True)
    def __and__(self, other):
        return self._from_apply("and", self, other)

    @typecheck_promote(lambda: Int, _reflect=True)
    def __lshift__(self, other):
        return self._from_apply("lshift", self, other)

    @typecheck_promote(lambda: (Int, Bool), _reflect=True)
    def __or__(self, other):
        return self._from_apply("or", self, other)

    @typecheck_promote(lambda: (Int, Bool))
    def __rand__(self, other):
        return self._from_apply("and", other, self)

    @typecheck_promote(lambda: Int)
    def __rlshift__(self, other):
        return self._from_apply("lshift", other, self)

    @typecheck_promote(lambda: (Int, Bool))
    def __ror__(self, other):
        return self._from_apply("or", other, self)

    @typecheck_promote(lambda: Int)
    def __rrshift__(self, other):
        return self._from_apply("rshift", other, self)

    @typecheck_promote(lambda: Int)
    def __rshift__(self, other):
        return self._from_apply("rshift", self, other)

    @typecheck_promote(lambda: (Int, Bool))
    def __rxor__(self, other):
        return self._from_apply("xor", other, self)

    @typecheck_promote(lambda: (Int, Bool), _reflect=True)
    def __xor__(self, other):
        return self._from_apply("xor", self, other)


@serializable()
class Float(Number):
    """
    Proxy float.

    Examples
    --------
    >>> from descarteslabs.workflows import Float
    >>> my_float = Float(2.3)
    >>> my_float
    <descarteslabs.workflows.types.primitives.number.Float object at 0x...>
    >>> other_float = Float(5.6)
    >>> val = my_float + other_float
    >>> val.compute() # doctest: +SKIP
    7.9
    >>> val = my_float > other_float
    >>> val.compute() # doctest: +SKIP
    False
    """

    _pytype = float
