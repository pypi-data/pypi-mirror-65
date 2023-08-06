#! /usr/bin/env python3
"""This module defines the base subject functionalities for the pub-sub-python
"""


__version__ = '1.0.0.0'
__author__ = 'Midhun C Nair <midhunch@gmail.com>'
__maintainers__ = [
    'Midhun C Nair <midhunch@gmail.com>',
]


import threading

from threading import Thread
from time import sleep
from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed,
)

from ps_py.utils import (
    import_string,
)


class BaseSubject:
    """Defines a subject to which anyone can subscribe to.
    """
    _publisher = None

    def __new__(cls, subject, *args, initial_value=None, **kwargs):
        """
        """
        Publisher = import_string('ps_py.publisher.Publisher')
        pub = Publisher()
        name = subject if not callable(subject) else id(subject)
        if name not in pub.subjects:
            pub.subjects[name] = super().__new__(cls)
            pub.subjects[name]._publisher = pub
            pub.subjects[name].SubscriberClass = import_string('ps_py.subscriber.Subscriber')
            pub.subjects[name].PublisherClass = Publisher
            pub.subjects[name]._lock = threading.Lock()
            pub.subjects[name]._pipe = None
            pub.subjects[name].name = name
        else:
            if initial_value is not None:
                pub.subjects[name].next(initial_value)

        return pub.subjects[name]

    def __init__(self, subject, initial_value=None):
        """
        """
        self.subject = subject
        self.initial_value = initial_value
        self.value = initial_value

    @property
    def publisher(self):
        """
        """
        if not isinstance(self._publisher, self.PublisherClass):
            self._publisher = self.PublisherClass()
        return self._publisher

    @property
    def subject(self):
        """
        """
        return self._subject

    @subject.setter
    def subject(self, value):
        """
        """
        self._subject = value

    def subscribe(self, onSuccess, onError=None):
        """
        """
        sub = self.SubscriberClass(subject=self, onSuccess=onSuccess, onError=onError)
        # subscriber gets added to the instance on creation automatically.
        return sub

    def add_subscriber(self, subscriber):
        """
        """
        if not isinstance(subscriber, self.SubscriberClass):
            raise ValueError(
                "Expected value of type Subscriber but got %s." % type(subscriber)
            )
        self._lock.acquire()
        self.subscribers[subscriber.name] = subscriber
        subscriber.subject = self
        self._lock.release()
        if not (
            self.value is None
            and self.value == self.initial_value
        ):
            self.call_target(subscriber.success, self.value)

    def pipe(self, *args):
        """
        """
        item = None
        for arg in args:
            item = self.add_pipe(arg)

        if not (
            self.value is None
            and self.value == self.initial_value
        ):
            self.call_target(self._pipe.onSuccess, self.value)


        return item

    def add_pipe(self, item):
        """
        """
        from ps_py.contrib import (
            Map,
        )
        if not (
            isinstance(item, Map)
        ):
            raise ValueError(
                "Expected value of type Map but got type %s" % type(item)
            )

        self.pipes.append(item)

        if self._pipe is None:
            self._pipe = item
        else:
            self._pipe.add_pipe(item)

        return item

    def call_target(self, target, *args, executer=None, **kwargs):
        """
        """
        if executer is None:
            thread = Thread(
                target=target,
                args=args,
                kwargs=kwargs,
            )
            thread.daemon = True
            thread.start()
            return thread
        else:
            return executer.submit(target, *args, **kwargs)

    def call_on_success(self, value, executer=None):
        """
        """
        calls = []
        self._lock.acquire()
        if self._pipe is not None:
            calls.append(
                self.call_target(
                    self._pipe.onSuccess,
                    value,
                    executer=executer,
                )
            )

        for sub in self.subscribers.values():
            calls.append(
                self.call_target(
                    sub.success,
                    value,
                    executer=executer
                )
            )
        self._lock.release()
        return calls

    def call_on_error(self, error, executer=None):
        """
        """
        calls = []
        self._lock.acquire()
        if self._pipe is not None:
            calls.append(
                self.call_target(
                    self._pipe.onError,
                    error,
                    executer=executer,
                )
            )

        for sub in self.subscribers.values():
            calls.append(
                self.call_target(
                    sub.error,
                    error,
                    executer=executer
                )
            )
        self._lock.release()

        return calls

    def next(self, value, error=False):
        """This will take the new value to and send
        that to all the subscribers
        """
        def run(threads):
            with ThreadPoolExecutor(5) as executer:
                try:
                    self._lock.acquire()
                    self.value = value
                    self._lock.release()
                    if not error:
                        threads.extend(self.call_on_success(value, executer=executer))
                    else:
                        threads.extend(self.call_on_error(value, executer=executer))
                except Exception as err:
                        threads.extend(self.call_on_error(err, executer=executer))
        calls = []
        thread = Thread(
            target=run,
            args=(calls,),
            kwargs={},
        )
        thread.daemon = True
        thread.start()

        # return calls

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

    @property
    def pipes(self):
        """
        """
        try:
            if not isinstance(self._pipes, list):
                self._pipes = []
        except AttributeError:
            self._pipes = []

        return self._pipes

    @property
    def value(self):
        """
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        """
        self._value = value

    def unsubscribe(self, subscriber):
        """
        """
        del self.subscribers[subscriber.name]
        del subscriber
