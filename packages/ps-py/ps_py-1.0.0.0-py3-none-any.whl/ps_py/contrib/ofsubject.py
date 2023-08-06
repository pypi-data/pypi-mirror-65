#! /usr/bin/env python3
"""This module will define the Of functionality for pub-sub-python package
"""


__version__ = '1.0.0.0'
__author__ = 'Midhun C Nair <midhunch@gmail.com>'
__maintainers__ = [
    'Midhun C Nair <midhunch@gmail.com>',
]


from threading import Thread
from uuid import uuid4
from time import sleep

from ps_py.subject import Subject
from ps_py.utils import (
    get_unique_id,
)


class Of:
    """
    """
    def __init__(self, *args, timeout=5):
        """
        """
        self.id = str(uuid4())
        self.int_id = get_unique_id(self.id)[0]
        self.subject = Subject(self.int_id, initial_value=None)

        self.args = args
        self.index = -1
        self.timeout = timeout

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

    def subscribe(self, onSuccess, onError=None):
        """
        """
        sub = self.subject.subscribe(onSuccess=onSuccess, onError=onError)
        self.subscribers[sub.name] = sub
        if self.index == -1:
            self.run()
        return sub

    def run(self):
        """
        """
        self.index = 0
        def _run():
            """
            """
            for item in self.args:
                self.subject.next(item)
                sleep(self.timeout)

        thread = Thread(target=_run)
        thread.daemon = True
        thread.start()
        # thread.join()

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
