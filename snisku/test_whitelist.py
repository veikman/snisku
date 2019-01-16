# -*- coding: utf-8 -*-
"""Unit tests for the whitelist module, using pytest."""

###########
# IMPORTS #
###########


# Third party:
import pytest

# Local:
from .exc import ValidationFailure
from .whitelist import WhitelistOption
from .whitelist import WhitelistParameter
from .kvs import KeyValueStore


#########
# TESTS #
#########


def test_two_strings():
    o0 = WhitelistOption('a')
    o1 = WhitelistOption('b')
    param = WhitelistParameter(key='p', options=[o0, o1], default=o0.value)

    kvs = KeyValueStore()
    assert param.retrieve(kvs) == 'a'

    param.store(kvs, 'b')
    assert param.retrieve(kvs) == 'b'

    param.store(kvs, o1.value)
    assert param.retrieve(kvs) == 'b'

    param.store(kvs, 'c')
    with pytest.raises(ValidationFailure):
        param.retrieve(kvs)
