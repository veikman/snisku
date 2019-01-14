# -*- coding: utf-8 -*-
"""Exceptions."""


class ParameterError(Exception):
    """A base class for errors in parsing and validating Snisku parameters."""


class ParserError(TypeError, ParameterError):
    """A signal that a serialized or candidate value cannot be parsed."""


class ValidatorError(ValueError, ParameterError):
    """A signal that a validator has encountered an internal error."""


class ValidationFailure(ValueError, ParameterError):
    """A signal that a validator has rejected a candidate value."""
