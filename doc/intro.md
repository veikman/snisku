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

Snisku parameters are stateless. They never store anything like a current
value. They only coordinate the storage and retrieval of parameters in various
ways.

## Further reading

Other documents in this project:

* On [side effects](sidefx.md).

This does not cover every feature of Snisku, nor does it go into detail. Snisku
code has extensive built-in documentation and type annotations for ease of use
and deeper learning.
