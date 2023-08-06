#! /usr/bin/env python3
"""This module defines the utility functionalities for the pub-sub-python
"""


__all__ = [
    'get_unique_id',
    'import_string',
]
__version__ = '1.0.0.0'
__author__ = 'Midhun C Nair <midhunch@gmail.com>'
__maintainers__ = [
    'Midhun C Nair <midhunch@gmail.com>',
]


from hashlib import (
    md5,
)
from importlib import (
    import_module
)


DIGITS = 8
BASE_16 = 16


def get_unique_id(key):
    """computes the crc of agiven key with md5 algo
    and computes a unique base 16 evaluation of last
    DIGITS (specified by const DIGITS).
    Returns both the base 16 and crc.
    """
    crc = md5(
        key.encode('utf-8')
    ).hexdigest()

    return (
        int(
            crc[-DIGITS:],
            BASE_16
        ),
        crc
    )


def import_string(py_path):
    """Tries to import the attribute of a module (function/class/...)
    """
    try:
        m_path, a_name = py_path.rsplit('.', 1)
    except ValueError as err:
        raise ImportError("%s doesn't seem to be a valid python path" % py_path) from err

    module = import_module(m_path)

    try:
        return getattr(module, a_name)
    except AttributeError as err:
        raise ImportError(
            "Module %s doesn't seem to have an attribute with name %s" % (
                m_path,
                a_name,
            )
        ) from err
