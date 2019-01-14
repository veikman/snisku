# -*- coding: utf-8 -*-
"""Unit tests for the param module, using pytest."""

###########
# IMPORTS #
###########


# Local:
from .param import Parameter


#########
# TESTS #
#########


def test_integer_retrieval_trivial():
    p = Parameter(key='a', parser=int, validator=lambda v: isinstance(v, int))
    kvs = dict(a=1)
    v = p.retrieve(kvs)
    assert v == 1


def test_integer_retrieval_from_string():
    p = Parameter(key='a', parser=int, validator=lambda v: isinstance(v, int))
    kvs = dict(a="2")
    v = p.retrieve(kvs)
    assert v == 2
