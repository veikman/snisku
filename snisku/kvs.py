# -*- coding: utf-8 -*-
"""Key-value storage of parameters."""

###########
# IMPORTS #
###########


# Standard:
import json

# Third party:
from pydispatch import dispatcher


#############
# INTERFACE #
#############


class KeyValueStore(dict):
    """A dict with a few conveniences for serialization.

    This is intended as a snapshot of primitive keys to primitive values. These
    are not packaged for immediate use but rather intended for serialization,
    transport and logging. For example, a Gunka unit may take a KeyValueStore
    as one of its inputs.

    Parameter objects get their values from a KeyValueStore at need. This
    process may produce rich output, but a KeyValueStore cannot, by itself,
    produce richer representations of its raw data.

    """

    def dump(self, filepath, handler=json.dump):
        """Dump the contents to named file. Return None."""
        with open(filepath, mode='w') as f:
            handler(self, f)

    def load(self, filepath, handler=json.load,
             merge=True, new_only=True, signal=True):
        """Load contents of file into self. Also return the contents."""
        with open(filepath, mode='r') as f:
            contents = handler(f)

        for key, value in contents.copy().items():
            if new_only and key in self and value == self[key]:
                # The value is not new. Ignore it.
                contents.pop(key)
                continue
            if merge:
                # Write to self.
                self[key] = value
            if signal:
                # Signal change.
                self._signal(key, merge=merge, new_value=value)

        return contents

    def clear(self, signal=True):
        """Extend parent method for signalling."""
        prior_keys = set(self.keys())
        super().clear()
        if signal:
            # Signal change.
            for key in prior_keys:
                self._signal(key, reset=True)

    def _signal(self, key, **kwargs):
        """Invite or provoke side effects by sending a signal.

        In this default implementation, this method sends a parameter-specific
        signal using pydispatch. Interested parties must be connected by key
        to receive such a signal.

        The use of pydispatch here should be considered an implementation
        detail and may change in a future version of Snisku.

        The intended use of this method is to update a GUI with new values
        as they are loaded from a file.

        """
        dispatcher.send(signal=key, sender=self, **kwargs)
