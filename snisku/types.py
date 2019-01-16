# -*- coding: utf-8 -*-
"""Implementations of BaseParameter for various common data types."""

#############
# IMPORTS #
#############


# Third party:
import arrow

# Local:
from .param import BaseParameter


#############
# INTERFACE #
#############


class BooleanParameter(BaseParameter):
    """A Boolean parameter."""

    def __init__(self, parser=bool, **kwargs):
        super().__init__(parser=parser, **kwargs)

    def toggle(self, kvs):
        """Toggle the value of the parameter in passed key-value store."""
        self.store(kvs, not self.retrieve(kvs))


class AnyIntegerParameter(BaseParameter):
    """An integer parameter."""

    def __init__(self, parser=int, **kwargs):
        super().__init__(parser=parser, **kwargs)


class NonnegativeParameter(BaseParameter):
    """A numeric parameter that can’t be negative."""

    def __init__(self, validator=lambda v: v >= 0, **kwargs):
        """Inject a default validator but no purpose."""
        super().__init__(validator=validator, **kwargs)


class NonnegativeIntegerParameter(AnyIntegerParameter, NonnegativeParameter):
    """An integer parameter that has to be non-negative."""


class ArrowParameter(BaseParameter):
    """A parameter representing a date and time using Arrow."""

    def __init__(self, parser=arrow.get, dumper=lambda a: a.for_json(),
                 **kwargs):
        super().__init__(parser=parser, dumper=dumper, **kwargs)
