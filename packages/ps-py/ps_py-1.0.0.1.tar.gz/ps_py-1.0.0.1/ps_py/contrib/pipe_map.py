#! /usr/bin/env python3
"""This module will define the map functionality for pub-sub-python package
"""


__version__ = '1.0.0.1'
__author__ = 'Midhun C Nair <midhunch@gmail.com>'
__maintainers__ = [
    'Midhun C Nair <midhunch@gmail.com>',
]


from uuid import uuid4

from ps_py.subject import BaseSubject


class Map(BaseSubject):
    def __init__(
        self,
        subject,
        *args,
        initial_value=None,
        success=None,
        error=None,
        **kwargs
    ):
        """
        """
        self.subject = subject
        self.initial_value = initial_value
        self.value = initial_value
        self._args = args
        self._kwargs = kwargs
        self.index = -1

        self.mapSub = self.subscribe(onSuccess=success, onError=error)
        del self.subscribers[self.mapSub.name]

    def onSuccess(self, value):
        """
        """
        self.next(self.mapSub.success(value))

    def onError(self, error):
        """
        """
        self.next(self.mapSub.error(value), error=True)


def map(onSuccess, onError=None):
    """
    """
    if not callable(onSuccess):
        raise ValueError(
            "Expecting a callable but got type %s" % (type(onSuccess))
        )

    if onError is not None and not callable(onError):
        raise ValueError(
            "Expecting a callable but got type %s" % (type(onError))
        )
    elif callable(onError):
        pass
    else:
        onError = lambda error: None

    return Map(subject=str(uuid4()), success=onSuccess, error=onError)
