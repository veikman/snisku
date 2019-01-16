# -*- coding: utf-8 -*-
"""User-interface data management for Snisku objects."""

#############
# INTERFACE #
#############


class UserInterfacePresenter(object):
    """A simple collection of texts for presenting an item in a UI.

    This model does not, in itself, prefer, require or process any markup.

    """

    def __init__(self, name: str = None, summary: str = None,
                 explanation: str = None) -> None:
        """Initialize. Store passed optional strings.

        The strings should be progressively longer and should not repeat one
        another. The ‘name’ should be in sentence case without concluding
        punctuation, hence usable as a list item or heading. The ‘summary’
        should be one complete paragraph with punctuation. The ‘explanation’
        should be multiple paragraphs.

        """
        self.name = name
        self.summary = summary
        self.explanation = explanation
