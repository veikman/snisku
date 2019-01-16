# -*- coding: utf-8 -*-
"""An implementation of BaseParameter for a whitelist."""

#############
# IMPORTS #
#############


# Standard library:
from typing import Any
from typing import Callable
from typing import Hashable
from typing import Iterable

# Local:
from .param import BaseParameter
from .ui import UserInterfacePresenter


#############
# INTERFACE #
#############


class WhitelistOption(object):
    """A single option permissible for a WhitelistParameter."""

    def __init__(self, value: Hashable, ui: Any = None) -> None:
        """Initialize.

        ‘value’ should be hashable and serializable like any Snisku parameter
        value. If something heavier is needed, subclass WhitelistOption to add
        it as a secondary value and make an appropriate parser, dumper and
        validator to translate between the two.

        The optional ‘ui’ parameter can be a snisku.ui.UserInterfacePresenter
        with a name for the option, but does not have to be.

        """
        self.value = value
        self.ui = ui


class OptionWhitelist(list):
    """An exhaustive list of options for a WhitelistParameter."""

    def by_value(self, value):
        """Look up an option by its value. O(n)."""
        for option in self:
            if option.value == value:
                return option
        raise KeyError('Value ‘{}’ is not whitelisted.')


class WhitelistParameter(BaseParameter):
    """A parameter that allows only specific values."""

    def __init__(self,
                 options: Iterable[WhitelistOption] = None,
                 validator: Callable[[Any], bool] = None,
                 **kwargs: Any) -> None:
        """Initialize.

        Store passed options as an OptionWhitelist.

        Make a validator if none is supplied.

        """
        assert options is not None
        if not isinstance(options, OptionWhitelist):
            options = OptionWhitelist(options)
        self.options = options

        if validator is None:
            def validator(value):
                try:
                    self.options.by_value(value)
                except KeyError:
                    return False
                else:
                    return True

        super().__init__(validator=validator, **kwargs)


# An example: A generic option for disabling a parameter.
none = WhitelistOption(None, ui=UserInterfacePresenter(name='Disabled'))
