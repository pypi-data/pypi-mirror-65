#! /usr/bin/env python3
"""This module will define the Merge functionality for pub-sub-python package
"""


__version__ = '1.0.0.0'
__author__ = 'Midhun C Nair <midhunch@gmail.com>'
__maintainers__ = [
    'Midhun C Nair <midhunch@gmail.com>',
]


from uuid import uuid4

from pspy.subject import Subject
from pspy.subscriber import Subscriber
from pspy.utils import (
    get_unique_id,
)


class Merge:
    """This will allow us to merge multiple subscriptions to one.
    Expects Subcriber iterables.
    """
    def __init__(self, *args):
        """
        """
        self.id = str(uuid4())
        self.int_id = get_unique_id(self.id)[0]
        self.subject = Subject(self.int_id, initial_value=None)

        self.args = args
        for sub in self.args:
            self.add(sub)

    @property
    def args(self):
        """
        """
        return self._args

    @args.setter
    def args(self, value):
        """
        """
        if (
            isinstance(value, str)
            or not hasattr(value, '__iter__')
        ):
            raise ValueError("Expected an iterable value but got type '%s'" % type(value))
        self._args = value

    def add(self, sub):
        """
        """
        if isinstance(sub, Subscriber):
            subject = sub.subject
        elif isinstance(sub, Subject):
            subject = sub
        else:
            raise ValueError(
                "Expected an value of type Subscriber|Subject but got %s" % type(sub)
            )

        sub.subscribe(onSuccess=self.onSuccess, onError=self.onSuccess)

    def subscribe(self, onSuccess, onError=None):
        """
        """
        sub = self.subject.subscribe(onSuccess=onSuccess, onError=onError)
        self.subscribers[sub.name] = sub
        return sub

    def onSuccess(self, value):
        """
        """
        self.subject.next(value)

    def onError(self, error):
        """
        """
        self.subject.next(error, error=True)

    def pipe(self, *args):
        """
        """
        return self.subject.pipe(*args)

    @property
    def subscribers(self):
        """
        """
        try:
            if not isinstance(self._subscribers, dict):
                self._subscribers = {}
        except AttributeError:
            self._subscribers = {}

        return self._subscribers
