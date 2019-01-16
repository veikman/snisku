# -*- coding: utf-8 -*-
"""Snisku parameters. Base module."""

###########
# IMPORTS #
###########


# Standard:
from typing import Any
from typing import Callable
from typing import Hashable

# Third party:
from pydispatch import dispatcher

# Local:
from .exc import ParameterError
from .exc import ParserError
from .exc import ValidatorError
from .exc import ValidationFailure


#############
# INTERFACE #
#############


class BaseParameter(object):
    """A model of a parameter known to and needed in an application.

    Parameters are like flags to a command-line application. A parameter can
    have a default value, but the parameter itself does not store its current
    value. The parameter merely knows how to retrieve its current value when
    presented with a key-value store that is mutually independent of the
    parameter.

    """

    def __init__(self,
                 key: Hashable = None,
                 ui: Any = None,
                 default: Any = None,
                 parser: Callable[[Hashable], Any] = lambda v: v,
                 dumper: Callable[[Any], Hashable] = lambda v: v,
                 validator: Callable[[Any], bool] = lambda v: True) -> None:
        """Initialize.

        Terse help with arguments:

        * ‘key’: A unique identifier. Mandatory.

        * ‘ui’: Documentation for a user interface. Optional.

        * ‘default’: The default value of the parameter.

        * ‘parser’: A value parser.

        * ‘dumper’: A value dumper. The reverse of ‘parser’.

        * ‘validator’: A validator of parsed values.

        Additional help with arguments:

        * The ‘key’ argument must be hashable and is normally a string. Keys
          that are not easily serialized will require special treatment by
          key-value stores, as the Parameter’s own parser and dumper treat
          only values, not keys.

          ‘key’ is a keyword argument rather than a positional argument
          because, although ‘key’ is mandatory, where ‘ui’ is supplied, ‘ui’
          should be passed in first as human-readable documentation of the
          parameter in the code.

        * The ‘ui’ argument is expected to refer to a UserInterfacePresenter
          as defined in snisku.ui, but it may be any object serving a
          similar purpose. A TUI/GUI widget is not recommended.

          BaseParameter does not implement ‘__str__’ because it is agnostic
          about the presence and properties of ‘ui’.

        * If a ‘default’ value is not specified, ‘None’ will be stored.

          Any attempt to retrieve the parameter’s value from a key-value store
          will use the default in a simple call to ‘get’, such that no
          distinction is made between finding the default value in the
          key-value store and not finding any value there.

          To signify that no permissible default value exists, ensure that
          the parser and/or validator passed to this function will not accept
          the default value passed to this method. Such a relationship is
          checked in the ‘default_is_valid’ method.

        * The default ‘parser’ and ‘dumper’ are the identity function.
          These callables are applied only to values, not keys, and should be
          unary, pure functions (free of state and side effects) because they
          are public attributes and may be called outside of setting and
          writing  parameter values, as they are called in ‘default_is_valid’.

        * The default ‘validator’ always return True. The validator is
          conceptually similar to the parser in that it should be a unary,
          pure function, it is applied only to values, and it is public and
          used in ‘default_is_valid’.

        Parsers and validators are mutually distinct because they serve
        different purposes. The parser forces user input to conform to a data
        type, potentially omitting some data in the process. The validator
        checks whether a conformed value is permissible. These two functions
        will usually differ by domain and range and will often be independently
        reusable. This aspect of Snisku is function-oriented.

        Separating parsing from validation in this way keeps the API simple.
        It is not necessary for the user to build a combined parser and
        validator that must raise some particular exception to communicate
        information valuable to a troubleshooter, such as the circumstance that
        a value can be cast to an acceptable type yet is invalid. A standard
        Python ValueError would be ambiguous for this purpose: it can be
        omitted by a reasonably designed parser.

        """
        assert key is not None
        self.key = key
        self.ui = ui
        self.default = default
        assert callable(parser)
        self.parser = parser
        assert callable(dumper)
        self.dumper = dumper
        assert callable(validator)
        self.validator = validator

    def parse_and_validate(self, value, parser=None, validator=None):
        """Parse and validate passed value.

        Return a valid value for self or raise ParameterError.

        """
        parser = parser or self.parser
        validator = validator or self.validator

        try:
            refined = parser(value)
        except Exception as e:
            s = 'Could not parse ‘{!r}’ as a value for ‘{}’.'
            raise ParserError(s.format(value, self.key)) from e

        try:
            if validator(refined):
                return refined
        except Exception as e:
            s = 'Could not validate ‘{!r}’ as a value for ‘{}’.'
            raise ValidatorError(s.format(refined, self.key)) from e
        else:
            s = 'Value ‘{!r}’ is not valid for ‘{}’.'
            raise ValidationFailure(s.format(refined, self.key))

    def default_is_valid(self, **kwargs):
        """Return True if the built-in default is valid.

        This is intended for user interfaces that need to know whether to
        present a standard widget for resetting the parameter to its default
        value.

        """
        try:
            self.parse_and_validate(self.default, **kwargs)
        except ParameterError:
            return False
        else:
            return True

    def retrieve(self, kvs, **kwargs):
        """Retrieve a value for self from passed key-value store.

        This triggers parsing and validation. Return a valid value for self or
        raise ParameterError.

        """
        assert kvs is not None
        return self.parse_and_validate(kvs.get(self.key, self.default),
                                       **kwargs)

    def store(self, kvs, value, dumper=None, signal=True):
        """Dump passed value into passed key-value store."""
        dumper = dumper or self.dumper
        kvs[self.key] = dumper(value)
        if signal:
            # Signal change.
            self._signal(kvs, new_value=value)

    def reset(self, kvs, signal=True):
        """Remove any value of self from passed key-value store. Return None.

        The reset is selective: No other values are removed from the key-value
        store. Also note that the default value of the parameter, which is
        stored by the parameter and not in the key-value store, is unaffected
        by this action.

        If the key-value store has no value for the parameter, no change will
        occur and none will be signalled, nor will any exception be raised.

        """
        try:
            kvs.pop(self.key)
        except KeyError:
            pass
        else:
            if signal:
                # Signal change.
                self._signal(kvs, reset=True)

    def _signal(self, kvs, **kwargs):
        """Invite or provoke side effects by sending a signal.

        In this default implementation, this method sends a parameter-specific
        signal using pydispatch.

        The use of pydispatch here should be considered an implementation
        detail and may change in a future version of Snisku.

        The intended uses of this method include saving settings to a file.
        For that reason, the key-value store, not the parameter, is passed as
        the sender of the signal. Doing so enables subscription of changes to
        the store without making strict requirements upon the store.

        """
        dispatcher.send(signal=self.key, sender=kvs, **kwargs)
