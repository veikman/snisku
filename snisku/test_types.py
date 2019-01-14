# -*- coding: utf-8 -*-
"""Unit tests for the types module, using pytest."""

###########
# IMPORTS #
###########


# Third party:
import arrow

# Local:
from .types import ArrowParameter
from .kvs import KeyValueStore


#########
# TESTS #
#########


def test_store_retrieve_cycle():
    default = arrow.utcnow()
    param = ArrowParameter(key='t0', default=default)
    value = param.parser('2020-02-02')
    kvs = KeyValueStore()
    param.store(kvs, value)
    assert param.retrieve(kvs) == arrow.get('2020-02-02 00:00:00+00:00')
    param.reset(kvs)
    assert param.retrieve(kvs) == default
