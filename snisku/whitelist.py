# -*- coding: utf-8 -*-
"""A deprecated precursor to the option module.

This module will be removed in Snisku 1.0.0.

"""

#############
# IMPORTS #
#############


# Standard library:
from typing import Any
from typing import Hashable
from warnings import warn

# Local:
from .option import Option
from .option import ExhaustiveParameter
from .option import none  # noqa (0.2.0 backwards compatibily)


#############
# INTERFACE #
#############


class WhitelistOption(Option):
    """A single option permissible for a WhitelistParameter."""

    def __init__(self, value: Hashable, ui: Any = None) -> None:
        """Initialize."""
        warn('snisku.whitelist.WhitelistOption is deprecated in favour '
             'of snisku.option.Option', DeprecationWarning)
        super().__init__(value, ui)


class OptionWhitelist(list):
    """An exhaustive list of options for a WhitelistParameter."""

    def __init__(self, *args, **kwargs):
        warn('snisku.whitelist.OptionWhiteList is deprecated in favour '
             'of any tuple of snisku.option.Option', DeprecationWarning)
        super().__init__(*args, **kwargs)

    def by_value(self, value):
        """Look up an option by its value. O(n)."""
        for option in self:
            if option.value == value:
                return option
        raise KeyError('Value ‘{}’ is not whitelisted.')


class WhitelistParameter(ExhaustiveParameter):
    """Identical to ExhaustiveParameter but non-inclusively named."""

    def __init__(self, *args, **kwargs):
        warn('snisku.whitelist.WhitelistParameter is deprecated in favour '
             'of any tuple of snisku.option.ExhaustiveParameter',
             DeprecationWarning)
        super().__init__(*args, **kwargs)
