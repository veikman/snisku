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


class ArrowParameter(BaseParameter):
    """A parameter representing a date and time using Arrow."""

    def __init__(self, parser=arrow.get, dumper=lambda a: a.format(),
                 **kwargs):
        super().__init__(parser=parser, dumper=dumper, **kwargs)
