# -*- coding: utf-8 -*-
"""Unit tests for the argparse module, using pytest."""

###########
# IMPORTS #
###########


# Standard library:
from argparse import ArgumentParser
import math
from unittest.mock import patch

# Third party:
import pytest

# Local:
from .kvs import KeyValueStore
from .param import BaseParameter
from .types import BooleanParameter
from .types import AnyIntegerParameter
from .types import NonnegativeRealParameter
from .argparse import store_constant
from .argparse import store_variable
from .argparse import store_false
from .argparse import store_true


#########
# TESTS #
#########


def test_store_valid_variable():
    """A parser that takes any single value."""
    kvs = KeyValueStore()
    parameter = BaseParameter(key='k')
    parser = ArgumentParser()
    parser.add_argument('-p', action=store_variable(kvs, parameter))

    args = parser.parse_args(args=['-p', 'v'])
    assert args.p == 'v'
    assert parameter.retrieve(kvs) == 'v'

    kvs.clear()  # Clear state before parsing another set of arguments.

    args = parser.parse_args(args=[])
    assert args.p is None
    assert parameter.retrieve(kvs) is None


def test_store_invalid_variable():
    """Pass in a value that the Snisku parameter cannot take."""
    kvs = KeyValueStore()
    parameter = AnyIntegerParameter(key='k')
    parser = ArgumentParser()
    parser.add_argument('-p', action=store_variable(kvs, parameter))

    # First try a value that does work.
    args = parser.parse_args(args=['-p', '2'])
    assert args.p == 2
    assert parameter.retrieve(kvs) == 2

    # Reset.
    kvs.clear()

    # Expect argparse to try to exit its application while parsing a
    # bad candidate value.

    class Exit(Exception):
        pass

    with patch('argparse._sys.exit') as p:
        p.side_effect = Exit
        with pytest.raises(Exit):
            parser.parse_args(args=['-p', 'v'])


def test_store_single_constant():
    """A parser that predetermines a constant."""
    kvs = KeyValueStore()
    parameter = BaseParameter(key='k')
    parser = ArgumentParser()
    parser.add_argument('-p', action=store_constant(kvs, parameter), const='V')

    args = parser.parse_args(args=['-p'])
    assert args.p == 'V'
    assert parameter.retrieve(kvs) == 'V'


def test_store_alternatives():
    """A parser that can set a single parameter in three ways.

    Try two different flags for constants, and one invalid and one valid
    candidates on the command line.

    """
    kvs = KeyValueStore()
    parameter = NonnegativeRealParameter(key='k')
    parser = ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-e', dest='n', action=store_constant(kvs, parameter),
                       const=math.e)
    group.add_argument('--pi', dest='n', action=store_constant(kvs, parameter),
                       const=math.pi)
    group.add_argument('-n', dest='n', action=store_variable(kvs, parameter))

    assert not kvs
    args = parser.parse_args(args=['-e'])
    assert args.n == parameter.retrieve(kvs) == math.e

    kvs.clear()
    args = parser.parse_args(args=['--pi'])
    assert args.n == parameter.retrieve(kvs) == math.pi

    kvs.clear()

    class Exit(Exception):
        pass

    with patch('argparse._sys.exit') as p:
        p.side_effect = Exit
        with pytest.raises(Exit):
            parser.parse_args(args=['-n', '-1.1'])

    kvs.clear()
    args = parser.parse_args(args=['-n', '1.1'])
    assert args.n == 1.1 == parameter.retrieve(kvs) == 1.1


def test_store_false():
    """A parser that stores False."""
    kvs = KeyValueStore()
    parameter = BooleanParameter(key='k')
    parser = ArgumentParser()
    parser.add_argument('-p', action=store_false(kvs, parameter))

    args = parser.parse_args(args=['-p'])
    assert args.p is False
    assert parameter.retrieve(kvs) is False


def test_store_true():
    """A parser that stores True."""
    kvs = KeyValueStore()
    parameter = BooleanParameter(key='k')
    parser = ArgumentParser()
    parser.add_argument('-p', action=store_true(kvs, parameter))

    args = parser.parse_args(args=['-p'])
    assert args.p is True
    assert parameter.retrieve(kvs) is True


def test_store_inversion():
    """A parser where the argument name opposes the destination name."""
    kvs = KeyValueStore()
    parameter = BooleanParameter(key='k', default=True)
    parser = ArgumentParser()
    parser.add_argument('--no', dest='yes', default=parameter.default,
                        action=store_false(kvs, parameter))

    args = parser.parse_args(args=[])
    assert args.yes is True
    assert parameter.retrieve(kvs) is True

    args = parser.parse_args(args=['--no'])
    assert args.yes is False
    assert parameter.retrieve(kvs) is False
