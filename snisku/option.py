# -*- coding: utf-8 -*-
"""An implementation of BaseParameter for options.

Options describe values for parameters that are individually described by user
interface presenters, are especially common, are recommended or (with
ExhaustiveParameter) are the only values permitted.

"""

#############
# IMPORTS #
#############


# Standard library:
from dataclasses import dataclass
from typing import Any
from typing import Tuple

# Local:
from .param import BaseParameter
from .param import Validator
from .ui import UserInterfacePresenter


#############
# INTERFACE #
#############


@dataclass(frozen=True)
class Option(object):
    """A wrapper for a privileged setting.

    ‘value’ should be serializable by a parameter, like any Snisku parameter
    value. If something heavier is needed, subclass Option to add it as a
    secondary value and make an appropriate parser, dumper and validator to
    translate between the two.

    The optional ‘ui’ value can be a snisku.ui.UserInterfacePresenter with a
    name for the option, but does not have to be.

    """

    value: Any
    ui: Any


class OptionParameter(BaseParameter):
    """A parameter that can have options.

    In this implementation, the options are not presumed to be exhaustive. They
    are exposed as an instance attribute for use by a user interface.

    A typical usage would be in populating a list of radio buttons, where the
    final button includes an editor for setting an arbitrary value matching
    none of the options in self.options.

    """

    def __init__(self, options: Tuple[Option, ...] = (), **kwargs) -> None:
        """Initialize."""
        self.options = options
        super().__init__(**kwargs)


class ExhaustiveParameter(OptionParameter):
    """A parameter that allows only its registered options’ values."""

    def __init__(self, validator: Validator = None,
                 **kwargs: Any) -> None:
        """Initialize. Require options. Make a default validator."""
        if validator is None:
            def validator(value: Any) -> bool:
                return any((value == o.value for o in self.options))

        super().__init__(validator=validator, **kwargs)
        assert self.options


# An example of an Option: The value None, as used for disabling a parameter.
none = Option(None, UserInterfacePresenter(name='Disabled'))
