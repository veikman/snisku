# -*- coding: utf-8 -*-
"""Unit tests for the kvs module, using pytest."""

###########
# IMPORTS #
###########


# Local:
from .kvs import KeyValueStore


#########
# TESTS #
#########


def test_dump_empty_json_object(tmpdir):
    f = tmpdir.join('settings.json')
    KeyValueStore().dump(f)
    assert f.read() == '{}'


def test_dump_simple_json_object(tmpdir):
    f = tmpdir.join('settings.json')
    KeyValueStore(a=1).dump(f)
    assert f.read() == '{"a": 1}'


def test_load_empty_json_object(tmpdir):
    f = tmpdir.join('settings.json')
    f.write('{}')
    assert KeyValueStore().load(f) == dict()


def test_load_trivial_json_object(tmpdir):
    f = tmpdir.join('settings.json')
    f.write('{"a": 1}')
    assert KeyValueStore().load(f) == dict(a=1)
