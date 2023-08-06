#! /usr/bin/env python3
"""This module defines the base functionalities for the publisher  pub-sub-python
"""


__version__ = '1.0.0.0'
__author__ = 'Midhun C Nair <midhunch@gmail.com>'
__maintainers__ = [
    'Midhun C Nair <midhunch@gmail.com>',
]


from ps_py.utils import (
    import_string,
)


class BasePublisher:
    """Defines a BasePublisher who publishes the subjects.
    A SingleTon instance.
    """
    _subjects = {}
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        """
        if cls._instance is None:
            Subject = import_string('ps_py.subject.Subject')
            cls._instance = super().__new__(cls)
            cls._instance.SubjectClass = Subject

        return cls._instance

    def __init__(self, subject=None, args=None, kwargs=None):
        """
        """
        if subject is not None:
            args = args if args is not None else []
            kwargs = kwargs if kwargs is not None else {}
            if 'initial_value' not in kwargs:
                kwargs['initial_value'] = None
            self.add(subject, *args, **kwargs)

    @property
    def subjects(self):
        """
        """
        return self._subjects

    def get_subject(self, subject):
        """
        """
        return self.add(subject, initial_value=None)

    def add(self, subject, *args, initial_value=None, **kwargs):
        """
        """
        kwargs['initial_value'] = initial_value
        name = subject if not callable(subject) else id(subject)
        if name not in self.subjects:
            self.SubjectClass(subject, *args, **kwargs)  # automatically adds to self.subjects
        else:
            if kwargs['initial_value'] is not None:
                self.subjects[name].next(kwargs['initial_value'])

        return self.subjects[name]

    def subscribe(self, subject, onSuccess, onError=None):
        """
        """
        if isinstance(subject, self.SubjectClass):
            return subject.subscribe(onSuccess, onError)

        name = subject if not callable(subject) else id(subject)
        return self.subjects[name].subscribe(onSuccess, onError)

    def next(self, subject, value):
        """
        """
        if isinstance(subject, self.SubjectClass):
            return subject.next(value)

        name = subject if not callable(subject) else id(subject)
        return self.subjects[name].next(value)
