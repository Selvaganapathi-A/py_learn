from typing import Self


class SomeClass(object):
    def __init__(self: Self) -> None:
        """
        Called after the instance has been created (by `__new__()`),
        but before it is returned to the caller. The arguments are those passed
        to the class constructor expression. If a base class has an `__init__()` method,
        the derived class’s `__init__()` method, if any, must explicitly call it
        to ensure proper initialization of the base class part of the instance;
        for example: `super().__init__([args...])`"""
        super().__init__()
        super().__init_subclass__()

    def __init_subclass__(cls: type[Self]) -> None:
        """
        # `__init_subclass__`

        This method is called whenever the containing class is subclassed.
        `cls` is then the new subclass. If defined as a normal instance method,
        this method is implicitly converted to a class method.

        Keyword arguments which are given to a new class are passed to the parent
        class’s `__init_subclass__`. For compatibility with other classes using
        `__init_subclass__`, one should take out the needed keyword arguments
        and pass the others over to the base class, as in:

        ```python
        class Philosopher:
            def __init_subclass__(cls, /, default_name, **kwargs):
                super().__init_subclass__(**kwargs)
                cls.default_name = default_name

        class AustralianPhilosopher(Philosopher, default_name="Bruce"):
            pass
        ```

        The default implementation `object.__init_subclass__` does nothing,
        but raises an error if it is called with any arguments.

        """
        pass

    """
    The following methods can be defined to emulate numeric objects.
    Methods corresponding to operations that are not supported by the
    particular kind of number implemented (e.g., bitwise operations for
    non-integral numbers) should be left undefined.
    """

    def __add__(self, __other_value__: Self) -> Self:
        """
        # __add__

        This method implements `+` operator.
        """
        raise NotImplementedError()

    def __sub__(self, __other_value__: Self) -> bool:
        """
        # __sub__

        This method implements `-` operator.
        """
        raise NotImplementedError()

    def __mul__(self, __other_value__: Self) -> bool:
        """
        # __mul__

        This method implements `*` operator.
        """
        raise NotImplementedError()

    def __matmul__(self, __other_value__: Self) -> bool:
        """
        # __matmul__

        This method implements `@` operator.
        """
        raise NotImplementedError()

    def __truediv__(self, __other_value__: Self) -> bool:
        """
        # __truediv__

        This method implements `/` operator.
        """
        raise NotImplementedError()

    def __floordiv__(self, __other_value__: Self) -> bool:
        """
        # __floordiv__

        This method implements `//` operator.
        """
        raise NotImplementedError()

    def __mod__(self, __other_value__: Self) -> bool:
        """
        # __mod__

        This method implements `%` operator.
        """
        raise NotImplementedError()

    def __pow__(self, __other_value__: Self) -> bool:
        """
        # __pow__

        This method implements `**` operator.
        """
        raise NotImplementedError()

    def __lshift__(self, __other_value__: Self) -> bool:
        """
        # __lshift__

        This method implements `<<` operator.
        """
        raise NotImplementedError()

    def __rshift__(self, __other_value__: Self) -> bool:
        """
        # __rshift__

        This method implements `>>` operator.
        """
        raise NotImplementedError()

    def __and__(self, __other_value__: Self) -> bool:
        """
        # __and__

        This method implements `&` operator.
        """
        raise NotImplementedError()

    def __or__(self, __other_value__: Self) -> bool:
        """
        # __or__

        This method implements `|` operator.
        """
        raise NotImplementedError()

    def __xor__(self, __other_value__: Self) -> bool:
        """
        # __xor__

        This method implements `^` operator.
        """
        raise NotImplementedError()

    """Below methods are called to implement the augmented arithmetic
    assignments `(+=, -=, *=, @=, /=, //=, %=, **=, <<=, >>=, &=, ^=, |=)`.
    These methods should attempt to do the operation in-place
    (modifying self) and return the result (which could be, but does
    not have to be, self). If a specific method is not defined, or if that
    method returns NotImplemented, the augmented assignment falls back to
    the normal methods.
    For instance, if x is an instance of a class with an __iadd__() method,
    x += y is equivalent to x = x.__iadd__(y) . If __iadd__() does not
    exist, or if x.__iadd__(y) returns NotImplemented, x.__add__(y) and
    y.__radd__(x) are considered, as with the evaluation of x + y. In
    certain situations, augmented assignment can result in unexpected
    errors (see Why does a_tuple[i] += [‘item’] raise an exception when the
    addition works?), but this behavior is in fact part of the data model."""

    def __iadd__(self, __other_value__: Self) -> Self:
        """
        # __iadd__

        This method implements `+=` operator.
        """
        raise NotImplementedError()

    def __isub__(self, __other_value__: Self) -> bool:
        """
        # __isub__

        This method implements `-=` operator.
        """
        raise NotImplementedError()

    def __imul__(self, __other_value__: Self) -> bool:
        """
        # __imul__

        This method implements `*=` operator.
        """
        raise NotImplementedError()

    def __imatmul__(self, __other_value__: Self) -> bool:
        """
        # __imatmul__

        This method implements `@=` operator.
        """
        raise NotImplementedError()

    def __itruediv__(self, __other_value__: Self) -> bool:
        """
        # __itruediv__

        This method implements `/=` operator.
        """
        raise NotImplementedError()

    def __ifloordiv__(self, __other_value__: Self) -> bool:
        """
        # __ifloordiv__

        This method implements `//=` operator.
        """
        raise NotImplementedError()

    def __imod__(self, __other_value__: Self) -> bool:
        """
        # __imod__

        This method implements `%=` operator.
        """
        raise NotImplementedError()

    def __ipow__(self, __other_value__: Self) -> bool:
        """
        # __ipow__

        This method implements `**=` operator.
        """
        raise NotImplementedError()

    def __ilshift__(self, __other_value__: Self) -> bool:
        """
        # __ilshift__

        This method implements `<<=` operator.
        """
        raise NotImplementedError()

    def __irshift__(self, __other_value__: Self) -> bool:
        """
        # __irshift__

        This method implements `>>=` operator.
        """
        raise NotImplementedError()

    def __iand__(self, __other_value__: Self) -> bool:
        """
        # __iand__

        This method implements `&=` operator.
        """
        raise NotImplementedError()

    def __ior__(self, __other_value__: Self) -> bool:
        """
        # __ior__

        This method implements `|=` operator.
        """
        raise NotImplementedError()

    def __ixor__(self, __other_value__: Self) -> bool:
        """
        # __ixor__

        This method implements `^=` operator.
        """
        raise NotImplementedError()

    #
    """
    These methods are called to implement the binary arithmetic operations
    (+, -, *, @, /, //, %, divmod(), pow(), **, <<, >>, &, ^, |) with
    reflected (swapped) operands. These functions are only called if the
    left operand does not support the corresponding operation [3] and the
    operands are of different types. [4] For instance, to evaluate the
    expression x - y, where y is an instance of a class that has an
    __rsub__() method, type(y).__rsub__(y, x) is called if
    type(x).__sub__(x, y) returns NotImplemented.

    Note that ternary pow() will not try calling __rpow__()
    (the coercion rules would become too complicated).
    """

    def __radd__(self, __other_value__: Self) -> Self:
        """
        #  __radd__

        This method implements `+` operator.
        """
        raise NotImplementedError()

    def __rsub__(self, __other_value__: Self) -> bool:
        """
        #  __rsub__

        This method implements `-` operator.
        """
        raise NotImplementedError()

    def __rmul__(self, __other_value__: Self) -> bool:
        """
        #  __rmul__

        This method implements `*` operator.
        """
        raise NotImplementedError()

    def __rmatmul__(self, __other_value__: Self) -> bool:
        """
        #  __rmatmul__

        This method implements `@` operator.
        """
        raise NotImplementedError()

    def __rtruediv__(self, __other_value__: Self) -> bool:
        """
        #  __rtruediv__

        This method implements `/` operator.
        """
        raise NotImplementedError()

    def __rfloordiv__(self, __other_value__: Self) -> bool:
        """
        #  __rfloordiv__

        This method implements `//` operator.
        """
        raise NotImplementedError()

    def __rmod__(self, __other_value__: Self) -> bool:
        """
        #  __rmod__

        This method implements `%` operator.
        """
        raise NotImplementedError()

    def __rpow__(self, __other_value__: Self) -> bool:
        """
        #  __rpow__

        This method implements `**` operator.
        """
        raise NotImplementedError()

    def __rlshift__(self, __other_value__: Self) -> bool:
        """
        #  __rlshift__

        This method implements `<<` operator.
        """
        raise NotImplementedError()

    def __rrshift__(self, __other_value__: Self) -> bool:
        """
        #  __rrshift__

        This method implements `>>` operator.
        """
        raise NotImplementedError()

    def __rand__(self, __other_value__: Self) -> bool:
        """
        #  __rand__

        This method implements `&` operator.
        """
        raise NotImplementedError()

    def __ror__(self, __other_value__: Self) -> bool:
        """
        #  __ror__

        This method implements `|` operator.
        """
        raise NotImplementedError()

    def __rxor__(self, __other_value__: Self) -> bool:
        """
        #  __rxor__

        This method implements `^` operator.
        """
        raise NotImplementedError()

    """
    Below methods Called to implement the unary arithmetic operations (-, +, abs() and ~).
    """

    def __neg__(self) -> bool:
        """
        # __neg__

        This method returns `-` negative value.
        """
        raise NotImplementedError()

    def __pos__(self) -> bool:
        """
        # __pos__

        This method returns `+` positive value.
        """
        raise NotImplementedError()

    def __abs__(self) -> bool:
        """
        # __abs__

        This method returns `abs()` value.
        """
        raise NotImplementedError()

    def __invert__(self) -> bool:
        """
        # __invert__

        This method implements `~` operator.
        """
        raise NotImplementedError()

    """
    Below methods called to implement the built-in functions
    complex(), int() and float(). Should return a value of the
    appropriate type.
    """

    def __complex__(self) -> complex:
        """
        # __complex__

        This method returns `complex()` value.
        """
        raise NotImplementedError()

    def __int__(self) -> int:
        """
        # __int__

        This method returns `int()` value.
        """
        raise NotImplementedError()

    def __float__(self) -> float:
        """
        # __float__

        This method returns `float()` value.
        """
        raise NotImplementedError()

    """
    These are the so-called “rich comparison” methods. The correspondence
    between operator symbols and method names is as follows:
        x<y calls x.__lt__(y),
        x<=y calls x.__le__(y),
        x==y calls x.__eq__(y),
        x!=y calls x.__ne__(y),
        x>y calls x.__gt__(y), and
        x>=y calls x.__ge__(y).
    """

    def __lt__(self, __other_value__: Self) -> bool:
        """
        # __lt__

        This method implements `<` operator.
        """
        raise NotImplementedError()

    def __le__(self, __other_value__: Self) -> bool:
        """
        # __le__

        This method implements `<=` operator.
        """
        raise NotImplementedError()

    def __eq__(self, __other_value__: Self) -> bool:
        """
        # __eq__

        This method implements `==` operator.
        """
        raise NotImplementedError()

    def __ne__(self, __other_value__: Self) -> bool:
        """
        # __ne__

        This method implements `!=` operator.
        """
        raise NotImplementedError()

    def __gt__(self, __other_value__: Self) -> bool:
        """
        # __gt__

        This method implements `>` operator.
        """
        raise NotImplementedError()

    def __ge__(self, __other_value__: Self) -> bool:
        """
        # __ge__

        This method implements `>=` operator.
        """
        raise NotImplementedError()

    def __not__(self) -> bool:
        """
        # __not__

        Return the outcome of `not` obj. Affected by `bool()` and `len()`.
        """
        raise NotImplementedError()

    def __contains__(self, __other_value__: Self) -> bool:
        raise NotImplementedError()

    def __getitem__(self, __other_value__: Self) -> bool:
        raise NotImplementedError()
        ...

    def __setitem__(self, __other_value__: Self) -> bool:
        raise NotImplementedError()

    def __delitem__(self, __other_value__: Self) -> bool:
        raise NotImplementedError()

    def __call__(self, __other_value__: Self) -> bool:
        raise NotImplementedError()

    def __enter__(self, __other_value__: Self) -> bool:
        raise NotImplementedError()

    def __exit__(self, __other_value__: Self) -> bool:
        raise NotImplementedError()

    def __aenter__(self, __other_value__: Self) -> bool:
        raise NotImplementedError()

    def __aexit__(self, __other_value__: Self) -> bool:
        raise NotImplementedError()

    def __iter__(self, __other_value__: Self) -> bool:
        raise NotImplementedError()

    def __next__(self, __other_value__: Self) -> bool:
        raise NotImplementedError()

    def __aiter__(self, __other_value__: Self) -> bool:
        raise NotImplementedError()

    def __anext__(self, __other_value__: Self) -> bool:
        raise NotImplementedError()

    def __await__(self, __other_value__: Self) -> bool:
        raise NotImplementedError()

    def __bool__(self) -> bool:
        raise NotImplementedError()

    def __len__(self):
        return 1020
