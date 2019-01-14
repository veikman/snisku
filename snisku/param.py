# -*- coding: utf-8 -*-
"""Snisku parameters."""

###########
# IMPORTS #
###########


# Local:
from .exc import ParserError
from .exc import ValidatorError
from .exc import ValidationFailure


#############
# INTERFACE #
#############


class Parameter():
    """A model of a parameter known to and needed in an application."""

    def __init__(self, key=None, default=None,
                 parser=lambda v: v, dumper=lambda v: v,
                 validator=lambda v: True,
                 title=None, description=None):
        self.key = key
        self.default = default
        self.parser = parser
        self.dumper = dumper
        self.validator = validator

    def retrieve(self, kvs, parser=None, validator=None):
        """Retrieve a value for self from passed key-value store.

        This triggers parsing and validation. Return a valid value for self or
        raise ParameterError.

        """
        parser = parser or self.parser
        validator = validator or self.validator

        raw = kvs.get(self.key, self.default)

        try:
            refined = parser(raw)
        except Exception as e:
            s = 'Could not parse ‘{!r}’ as a value for ‘{}’.'
            raise ParserError(s.format(raw, self.key)) from e

        try:
            if validator(refined):
                return refined
        except Exception as e:
            s = 'Could not validate ‘{!r}’ as a value for ‘{}’.'
            raise ValidatorError(s.format(refined, self.key)) from e
        else:
            s = 'Value ‘{!r}’ is not valid for ‘{}’.'
            raise ValidationFailure(s.format(refined, self.key))

    def store(self, kvs, value, dumper=None, signal=True):
        """Dump passed value into passed key-value store."""
        dumper = dumper or self.dumper
        kvs[self.key] = dumper(value)

    def reset(self, kvs):
        """Remove any value of self from passed key-value store.

        A new attempt to retrieve self from the store will return the default
        value of self. In that way, this is a selective reset action.

        """
        try:
            kvs.pop(self.key)
        except KeyError:
            pass
