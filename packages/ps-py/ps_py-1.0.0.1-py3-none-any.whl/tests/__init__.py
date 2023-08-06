#! /usr/bin/env python3
"""This module implements init for the tests package of pub-sub-python
``time python3.5 -m unittest tests -v``
"""


# __all__ = []
__version__ = '1.0.0.1'
__author__ = 'Midhun C Nair <midhunch@gmail.com>'
__maintainers__ = [
    'Midhun C Nair <midhunch@gmail.com>',
]


from .test_subject import *
from .test_publisher import *
from .test_subscriber import *
from .test_contrib import *
