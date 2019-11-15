# A tour of side effects

This document continues from the [introduction](intro.md).

Snisku does not have a logger. Although it is object-oriented, it is not very
stateful. Instead, it is event-based. Its methods have minimal side effects:

* Some actions are signaled so that other parts of your application can react
  to changes.
* By command, Snisku can mutate collections and even read and write files to
  get and store the values of parameters.

In the current version, signaling happens through the `pydispatch` module, a
general third-party event routing library. Future versions may support other
dispatchers.

## Subscribing for signaling

In the following example, a subscriber is connected to the `vol` parameter to
call another function (`apply_volume_setting`).

```python
from pydispatch import dispatcher
from snisku.param import BaseParameter

vol = BaseParameter(key='output_volume')
current_settings = dict()

def react_to_change(new_value=None):
    apply_volume_setting(new_value)

dispatcher.connect(react_to_change, signal=vol.key, sender=current_settings)
vol.store(current_settings, 80)
```

Running this example will trigger a `NameError`, because `apply_volume_setting`
is not defined here. Nonetheless, we see that `react_to_change` is
indeed called with the new value. The `new_value` keyword parameter itself is
provided by Snisku.

This event-based mechanism is one way to build responsive user interfaces. Your
UI widgets can subscribe to changes in the parameters they expose.

You do not have to define event handlers. If you don’t want to use the
dispatching system, simply ignore it; it does nothing by default. If you use
signaling but there is some specific action you want to perform without it, you
can mute signaling just for that action:

```python
vol.store(current_settings, 10, signal=False)
```

## Mutation

In the last section’s examples, the calls to `vol.store` would all return
`None`. However, `current_settings` would have the new value `{'output_volume':
10}` in the last example. This is mutation: The passed `dict` has changed as a
side effect of calling `vol.store`.

Suppose we reuse the code of the previous example, but change the signature of
`react_to_change` to this:

```python
def react_to_change(sender=None):
    ...
```

This way we get the entire key-value store as an argument instead of just the
new value. This is not terribly useful with a `dict`, but Snisku provides a
richer class that can save a whole suite of parameters as their values change.

## File I/O

Here’s an update to the signaling example for saving parameters to a file.

```python
from pydispatch import dispatcher
from snisku.param import BaseParameter
from snisku.kvs import KeyValueStore

vol = BaseParameter(key='output_volume')
current_settings = KeyValueStore()

def react_to_change(sender=None):
    sender.dump('/tmp/volume_demo.json')

dispatcher.connect(react_to_change, signal=vol.key, sender=current_settings)
vol.store(current_settings, 70)
```

This creates the file `/tmp/volume_demo.json`, containing a valid JSON snapshot
of the entire key-value store, which is still just our one parameter and value:
`{"output_volume": 70}`. The `dump` method takes a `handler` argument, in case
you want something other than JSON.

### The virtues of `KeyValueStore`

`dump` is one of the conveniences on `KeyValueStore`, which is primarily a
`dict`. A Snisku KVS can be used in place of a plain `dict` for parameter
retrieval.

Another convenience on `KeyValueStore` is the `load` method. This corresponds
to `dump` and adds signaling. Just like `BaseParameter.store`,
`KeyValueStore.load` will emit signals as it loads new values from a file.

With `KeyValueStore`, your application can easily save and load snapshots and
react appropriately, parameter by parameter, as values (on file) change. This
is intended as a foundation for responsive UI and persistence across
application sessions. As long as different processes do not compete to write to
the same files, it is also a crude means of one-way interprocess communication.
