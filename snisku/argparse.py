# -*- coding: utf-8 -*-
"""CLI integration: argparse action types for Snisku.

This would have been simpler if the argparse module exposed its built-in
action types.

"""

###########
# IMPORTS #
###########


# Standard library:
from functools import partial
import argparse

# Local:
from snisku.exc import ParameterError


#############
# INTERFACE #
#############


class Setting(argparse.Action):
    """An argparse action that sets a Snisku parameter."""

    def __init__(self, setter, *args, type=None, **kwargs):
        super().__init__(*args, **kwargs)
        assert callable(setter)
        self.setter = setter

    def __call__(self, _, namespace, values, __):
        self.setter(values)
        setattr(namespace, self.dest, values)


class SetConstant(Setting):
    """An argparse action that sets a parameter to a fixed value."""

    def __init__(self, *args, nargs=None, **kwargs):
        super().__init__(*args, nargs=0, **kwargs)

    def __call__(self, _, namespace, __, *args):
        super().__call__(_, namespace, self.const, *args)


class SetFalse(SetConstant):
    """An argparse action that sets a parameter to False."""

    def __init__(self, *args, const=None, **kwargs):
        super().__init__(*args, const=False, **kwargs)


class SetTrue(SetConstant):
    """An argparse action that sets a parameter to True."""

    def __init__(self, *args, const=None, **kwargs):
        super().__init__(*args, const=True, **kwargs)


# Function-oriented helpers follow.
# These are intended to be called like this:
#
#   parser.add_argument('--flag', action=store_variable(kvs, param))
#
# They return an instance of an action class.
# Notice that they do not apply the default value of their Snisku parameter to
# the argparse argument, which would generally be desirable for
# synchronization. A future version of Snisku may add a general solution.

def store_variable(*args):
    """Make a Setting instance that stores one value from a CLI."""
    return _bridge(Setting, *args)


def store_constant(*args):
    """Make a SetConstant instance that stores one value if flagged."""
    return _bridge(SetConstant, *args)


def store_false(*args):
    """Make an action instance that stores False if flagged."""
    return _bridge(SetFalse, *args)


def store_true(*args):
    """Make an action instance that stores True if flagged."""
    return _bridge(SetTrue, *args)


############
# INTERNAL #
############


def _bridge(cls, kvs, parameter):
    """Prefigure the instantiation of an objected-oriented action model.

    Use a Snisku parameter parsing and validation in place of the normal
    argparse type mechanism.

    """
    def parse_and_validate(candidate):
        try:
            return parameter.parse_and_validate(candidate)
        except ParameterError as e:
            # Signal failure to argparse.
            raise argparse.ArgumentTypeError(str(e)) from e

    def instantiate(*args, **kwargs):
        action = cls(partial(parameter.store, kvs), *args, **kwargs)
        action.type = parse_and_validate
        return action

    return instantiate
