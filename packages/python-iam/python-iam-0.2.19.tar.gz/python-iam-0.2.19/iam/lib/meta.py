"""Declares programming helper functions."""
import functools
import types


class AttributeDispatcher:
    """Decorates a dispatching method on a class and provides an interface
    to register handler functions.
    """

    @classmethod
    def dispatch(cls, attname):
        """Decorates the dispatching method to inject `func` based on the
        internal mapping lookup using the attribute or method `attname` of
        the pre-decoration first positional argument to the decorated
        method.
        """
        def decorator_factory(func):
            return functools.wraps(func)(cls(attname, func))
        return decorator_factory

    def __init__(self, attname, dispatcher):
        self.dispatcher = dispatcher
        self.attname = attname
        self.handlers = {}

    def get_handler(self, obj):
        """Returns the appropriate handler based on the value of attribute
        `attname` on `obj`.
        """
        name = getattr(obj, self.attname)
        if callable(name):
            name = name()
        return self.handlers[name]

    def register(self, name):
        """Registers a handler to the dispatcher."""
        def decorator_factory(decoratable):
            self.handlers[name] = decoratable

            @functools.wraps(decoratable)
            def f(this, obj, *args, **kwargs):
                return self.get_handler(obj)(this, obj, *args, **kwargs)
            f.register = self.register
            return f
        return decorator_factory
