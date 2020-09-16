# -*- coding: utf-8 -*-
"""Unit tests for the option module, using pytest."""

###########
# IMPORTS #
###########


# Third party:
import pytest

# Local:
from .exc import ValidationFailure
from .option import Option
from .option import OptionParameter
from .option import ExhaustiveParameter
from .kvs import KeyValueStore


#############
# CONSTANTS #
#############


o0 = Option('a', None)
o1 = Option('b', None)


#########
# TESTS #
#########


def test_two_strings_nonexhaustive():
    param = OptionParameter(key='p', options=[o0, o1], default=o0.value)

    kvs = KeyValueStore()
    assert param.retrieve(kvs) == 'a'

    param.store(kvs, 'b')
    assert param.retrieve(kvs) == 'b'

    param.store(kvs, o1.value)
    assert param.retrieve(kvs) == 'b'

    param.store(kvs, 'c')
    assert param.retrieve(kvs) == 'c'


def test_two_strings_exhaustive():
    param = ExhaustiveParameter(key='p', options=[o0, o1], default=o0.value)

    kvs = KeyValueStore()
    assert param.retrieve(kvs) == 'a'

    param.store(kvs, 'b')
    assert param.retrieve(kvs) == 'b'

    param.store(kvs, o1.value)
    assert param.retrieve(kvs) == 'b'

    param.store(kvs, 'c')
    with pytest.raises(ValidationFailure):
        param.retrieve(kvs)
