# -*- coding: utf-8 -*-
"""Unit tests for the param module, using pytest."""

###########
# IMPORTS #
###########


# Third party:
import pytest

# Local:
from .param import BaseParameter as Parameter
from .exc import ParserError
from .exc import ValidatorError
from .exc import ValidationFailure


#########
# TESTS #
#########


def test_integer_retrieval_trivial():
    p = Parameter(key='a', parser=int)
    kvs = dict(a=1)
    v = p.retrieve(kvs)
    assert v == 1


def test_integer_retrieval_from_string():
    p = Parameter(key='a', parser=int)
    kvs = dict(a="2")
    v = p.retrieve(kvs)
    assert v == 2


def test_integer_parsing_failure_from_default():
    p = Parameter(key='a', parser=int)
    kvs = dict()
    with pytest.raises(ParserError):
        p.retrieve(kvs)


def test_integer_parsing_failure_from_kvs():
    p = Parameter(key='a', parser=int)
    kvs = dict(a="A")
    with pytest.raises(ParserError):
        p.retrieve(kvs)


def test_positive_integer_validation_failure():
    p = Parameter(key='a', parser=int, validator=lambda v: v > 0)
    kvs = dict(a=-1)
    with pytest.raises(ValidationFailure):
        p.retrieve(kvs)


def test_integer_validator_error():
    p = Parameter(key='a', parser=int, validator=lambda v: v / 0)
    kvs = dict(a=1)
    with pytest.raises(ValidatorError):
        p.retrieve(kvs)
