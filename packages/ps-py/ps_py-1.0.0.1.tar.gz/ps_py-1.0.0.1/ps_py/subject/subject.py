#! /usr/bin/env python3
"""This module defines the subject functionalities for the pub-sub-python
"""


__version__ = '1.0.0.1'
__author__ = 'Midhun C Nair <midhunch@gmail.com>'
__maintainers__ = [
    'Midhun C Nair <midhunch@gmail.com>',
]


from time import sleep
from threading import Thread
from concurrent.futures import (
    ThreadPoolExecutor,
)

from .base import BaseSubject


class Subject(BaseSubject):
    """
    """
    def __init__(self, subject, *args, initial_value=None, **kwargs):
        """
        """
        self.subject = subject
        self.initial_value = initial_value
        self.value = initial_value
        self._args = args
        self._kwargs = kwargs
        self.index = -1

    def subscribe(self, *args, **kwargs):
        """
        """
        sub = super().subscribe(*args, **kwargs)
        # subscriber gets added to the instance on creation automatically.
        if callable(self.subject) and self.index == -1:
            self.run()

        return sub

    def run(self):
        """
        """
        self.index = 0
        def _run():
            """
            """
            result = None

            with ThreadPoolExecutor(2) as executer:
                future = executer.submit(self.subject, *self._args, **self._kwargs)
                while not future.done():
                    sleep(1)
                result = future.result()

            self.next(result)

        thread = Thread(target=_run)
        thread.daemon = True
        thread.start()
