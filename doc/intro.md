# Introduction

Snisku provides a model of application parameters. Here, we’ll use the example
of sound output volume as a parameter tracked within an application, building
from a trivial implementation in this document to something safe and useful in
other documents.

## Trivial exploration

Snisku is object-oriented. Its parameters are objects. To create a parameter,
you instantiate a class with a
[hashable](https://docs.python.org/3/glossary.html) key, such as a string.

```python
from snisku.param import BaseParameter
vol = BaseParameter(key='output_volume')
```

The key is the only necessary argument. It is used to retrieve values for the
parameter. For example, a parameter can find a corresponding value by key in a
simple Python `dict`, also known as a hash map.

```python
value = vol.retrieve({vol.key: 100})
```

In this example, `value` will be the integer 100. `vol` will not be changed.

Snisku parameters are stateless. They never store a current value. They only
coordinate the storage and retrieval of values in various ways.

## Default values

Parameters can take an optional default value and will retrieve that value
in the absence of relevant input.

```python
vol = BaseParameter(key='output_volume', default=100)
vol.retrieve({vol.key: 65})   # Returns 65.
vol.retrieve({})              # Returns 100.
vol.retrieve({vol.key: 100})  # Returns 100.
vol.default                   # Returns 100.
```

## A word on architecture

The normal way to get the current value for a parameter is to call `retrieve`,
as in the last example. To do this, you need two things in scope:

* Your parameter itself.
* Your source of current values.

Because your parameters should be stateless, they can safely be global, e.g.
module-level interface properties imported into each module that needs them.

Your source of values can also be global, but this is usually not safe in a
large application, and not when different components of the application should
use specific, potentially differing values.

Consider, for example, an implementation of Snisku with Gunka, where one unit
of work inherits a key-value store from its parent and hybridizes it with some
new settings to make a new child unit that needs the new settings. For such an
application, the key-value store should be copied before the copy is
[mutated](sidefx.md) and passed down, so that each unit of work has settings
relevant to that unit, and cannot impact its upstream.

So: Global parameters, local values.

## Further reading

Other documents in this project:

* On [side effects](sidefx.md).
* On [safety mechanisms](safety.md), including typing.

This does not cover every feature of Snisku, nor does it go into detail. Snisku
code has extensive built-in documentation and type annotations for ease of use
and deeper learning.
