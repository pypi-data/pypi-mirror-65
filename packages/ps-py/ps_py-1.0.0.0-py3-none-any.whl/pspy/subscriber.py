#! /usr/bin/env python3
"""This module defines the subscriber functionalities for the pub-sub-python
"""


__version__ = '1.0.0.0'
__author__ = 'Midhun C Nair <midhunch@gmail.com>'
__maintainers__ = [
    'Midhun C Nair <midhunch@gmail.com>',
]


from functools import partial


class Subscriber:
    """Defines the subscriber object
    """
    def __init__(self, subject, onSuccess, onError=None, name=None):
        """
        """
        self.onSuccess = onSuccess
        self.onError = onError
        self.name = name
        self.subject = subject
        if self.name not in self.subject.subscribers:
            self.subject.add_subscriber(self)

    @property
    def name(self):
        """
        """
        return self._name

    @name.setter
    def name(self, value):
        """
        """
        if value is None:
            value = "%s:%s" % (id(self.onSuccess), id(self.onError))

        self._name = value

    @property
    def subject(self):
        """
        """
        return self._subject

    @subject.setter
    def subject(self, value):
        """
        """
        from .subject import BaseSubject
        if not isinstance(value, BaseSubject):
            raise ValueError("Expected subject of type BaseSubject but got %s" %(type(value)))
        self._subject = value

    @property
    def onSuccess(self):
        """
        """
        return self._onSuccess

    @onSuccess.setter
    def onSuccess(self, value):
        """
        """
        if value is not None:
            if not callable(value) and isinstance(value, dict) and 'func' in value:
                if not callable(value['func']):
                    raise ValueError(
                        "Expected a callable in key 'func' but got '%s'", type(
                            value['func']
                        )
                    )

                value['args'] = value['args'] if value['args'] is not None else tuple()
                value['kwargs'] = value['kwargs'] if 'kwargs' in value and value['kwargs'] is not None else {}
            elif callable(value):
                value = {
                    'func': value,
                    'args': tuple(),
                    'kwargs': {},
                }
            else:
                raise ValueError(
                    "Expected a callable for onSuccess but got %s" % type(value)
                )
        else:
            raise ValueError(
                "Expected a callable value for onSuccess but got NoneType"
            )

        value = partial(value['func'], *value['args'], **value['kwargs'])

        self._onSuccess = value

    @property
    def onError(self):
        """
        """
        return self._onError

    @onError.setter
    def onError(self, value):
        """
        """
        if value is not None:
            if not callable(value) and isinstance(value, dict) and 'func' in value:
                if not callable(value['func']):
                    raise ValueError(
                        "Expected a callable in key 'func' but got '%s'", type(
                            value['func']
                        )
                    )

                value['args'] = value['args'] if value['args'] is not None else tuple()
                value['kwargs'] = value['kwargs'] if value['kwargs'] is not None else {}
            elif callable(value):
                value = {
                    'func': value,
                    'args': tuple(),
                    'kwargs': {},
                }
            else:
                raise ValueError(
                    "Expected a callable|None for onError but got %s" % type(value)
                )
            value = partial(value['func'], *value['args'], **value['kwargs'])

        self._onError = value

    def success(self, value):
        """
        """
        if self.onSuccess is not None:
            return self.onSuccess(value=value)

    def error(self, error):
        """
        """
        if self.onError is not None:
            return self.onError(error=error)

    def unsubscribe(self):
        """
        """
        self.subject.unsubscribe(self)
