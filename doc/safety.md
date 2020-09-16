# Safety mechanisms

This document continues from the [introduction](intro.md).

Snisku is ready to work across file and network boundaries. To achieve this,
Snisku parameters dump serializable versions of given values and then read them
back (deserialize them), even when working with local data stores in memory.

Whenever a parameter stores a value, it’s supposed to transform that value in
such a way that it’s safe to transport. Similarly, parameters can parse values
from such safe types, and validate their values. This is not done by
introspection but by a handful of pure, explicit functions.

## Parsing and validation

For an example of this safety mechanism, let’s say we want an output volume
parameter that can only take integer values of zero or higher.

```python
from snisku.types import NonnegativeIntegerParameter as NIP
vol = NIP(key='output_volume')
```

A `NonnegativeIntegerParameter` can handle, and check, a variety of inputs.
Invalid inputs will raise exceptions defined by the package.

```python
vol.parse_and_validate(0)      # Returns 0.
vol.parse_and_validate('0')    # Returns 0.
vol.parse_and_validate(66.67)  # Returns 66.
vol.parse_and_validate([1])    # Raises snisku.exc.ParserError.
vol.parse_and_validate(-1)     # Raises snisku.exc.ValidationFailure.
```

### Errors

Notice that in the last example, we handle a string without error. If you’re
handling arbitrary user input, be prepared to deal with `ParserError` and
`ValidationFailure` for more exotic strings. In addition, an internal error in
a Snisku application can raise `ValidatorError`. All of these inherit from
`ParameterError` for ease of treatment.

## Dumping and loading

Snisku supports [Arrow](https://pypi.org/project/arrow/) for date and time.
Here’s an example of dumping and parsing with Arrow.

```python
from arrow import Arrow
from snisku.types import ArrowParameter
from snisku.kvs import KeyValueStore as KVS
kvs = KVS()
last = ArrowParameter(key='last_modification')
last.store(kvs, Arrow(year=1976, month=9, day=17, hour=14))
```

At this point in the example, `kvs` is `{'last_modification':
'1976-09-17T14:00:00+00:00'}`, mapping a string to a string, which is easy to
store and transport as JSON. No need to pickle more complex objects. Retrieving
the parameter automatically parses the string back into a rich Arrow object.

```python
last.retrieve(kvs)  # Returns <Arrow [1976-09-17T14:00:00+00:00]>.
```

It’s the parameter doing this, not the KVS.

## Overview of built-in types

Snisku itself provides some types of parameters in `snisku.types`:

* True/false: `BooleanParameter`.
* Numbers: `AnyIntegerParameter`, `NonnegativeParameter` and
  `NonnegativeIntegerParameter`, as well as equivalent classes for real
  numbers represented by floats.
* Date and time: `ArrowParameter`.

In addition, in `snisku.option`, there is an `OptionParameter` for
radio buttons, enums and such.

## Customization

Back to the volume example: A `NonnegativeIntegerParameter` will allow very
high values, even values that will be meaningless as measurements of output
volume.

```python
vol.parse_and_validate(2**64)  # Returns 18446744073709551616.
```

Let’s say we want a scale of 0 to 100. We can implement this with a custom
validator function passed when we initialize `NonnegativeIntegerParameter`:

```python
vol = NIP(key='output_volume', validator=lambda v: 100 >= v >= 0)
vol.parse_and_validate(2**64)  # Raises snisku.exc.ValidationFailure.
```

The validator is a pure function, not a class method, but if you want multiple
parameters that all use the same range of 0 to 100, you can define a class for
them:

```python
class ZeroTo100(NonnegativeIntegerParameter):
    def __init__(self, validator=lambda v: 100 >= v >= 0, **kwargs):
        super().__init__(validator=validator, **kwargs)
```

Similarly, functions for parsing and dumping values are also pure and simple.
