#! /usr/bin/env python3
"""This module tests the Subscriber's functionality
"""


# __all__ = []
__version__ = '1.0.0.1'
__author__ = 'Midhun C Nair <midhunch@gmail.com>'
__maintainers__ = [
    'Midhun C Nair <midhunch@gmail.com>',
]


import unittest

from time import sleep

from ps_py.subscriber import (
    Subscriber,
)
from ps_py.subject import Subject

from .constants import (
    NEXT_WAIT,
)


class TestSubscriberSuite(unittest.TestCase):
    """
    """
    def test_initialize_wrong_subject(self):
        """
        """
        with self.assertRaises(ValueError):
            Subscriber(
                'TestSubscriberSuite_test_initialize_wrong_subject',
                onSuccess=lambda value: None
            )

    def test_initialize_wrong_onSuccess_1(self):
        """
        """
        sub = Subject('TestSubscriberSuite_test_initialize_wrong_onSuccess_1')
        with self.assertRaises(ValueError):
            Subscriber(sub, onSuccess="onSuccess")

    def test_initialize_wrong_onSuccess_2(self):
        """
        """
        sub = Subject('TestSubscriberSuite_test_initialize_wrong_onSuccess_2')
        with self.assertRaises(ValueError):
            Subscriber(sub, onSuccess=None)

    def test_initialize_wrong_onSuccess_3(self):
        """
        """
        sub = Subject('TestSubscriberSuite_test_initialize_wrong_onSuccess_3')
        with self.assertRaises(ValueError):
            Subscriber(sub, onSuccess={})

    def test_initialize_wrong_onSuccess_4(self):
        """
        """
        sub = Subject('TestSubscriberSuite_test_initialize_wrong_onSuccess_4')
        with self.assertRaises(ValueError):
            Subscriber(sub, onSuccess={'func':'func'})

    def test_initialize_wrong_onError_1(self):
        """
        """
        sub = Subject('TestSubscriberSuite_test_initialize_wrong_onError_1')
        with self.assertRaises(ValueError):
            Subscriber(sub, onSuccess=lambda value: None, onError="onError")

    def test_initialize_wrong_onError_2(self):
        """
        """
        sub = Subject('TestSubscriberSuite_test_initialize_wrong_onError_2')
        with self.assertRaises(ValueError):
            Subscriber(sub, onSuccess=lambda value: None, onError={'func':'func'})

    def test_initialize_wrong_onError_3(self):
        """
        """
        sub = Subject('TestSubscriberSuite_test_initialize_wrong_onError_3')
        with self.assertRaises(ValueError):
            Subscriber(sub, onSuccess=lambda value: None, onError={})

    def test_initialize(self):
        """
        """
        sub = Subject('TestSubscriberSuite_test_initialize', initial_value='init_val')
        subs = Subscriber(sub, onSuccess=lambda value: None)
        self.assertEqual(id(sub), id(subs.subject))
        self.assertTrue(subs.name in sub.subscribers)

    def test_success_1(self):
        """
        """
        sub = Subject('TestSubscriberSuite_test_success_1', initial_value='init_val')
        test_val = False
        def on_success(value):
            nonlocal test_val
            test_val = value

        self.assertEqual(test_val, False)
        subs = Subscriber(sub, onSuccess=on_success)
        self.assertEqual(test_val, 'init_val')
        subs.success('new')
        self.assertEqual(test_val, 'new')

    def test_success_2(self):
        """
        """
        sub = Subject('TestSubscriberSuite_test_success_2', initial_value='init_val')
        test_args = None
        test_val = False
        test_kwargs = None
        def on_success(*args, value=None, **kwargs):
            nonlocal test_val, test_args, test_kwargs
            test_args = args
            test_val = value
            test_kwargs = kwargs

        self.assertEqual(test_val, False)
        test_tuple = (1, 2, 3)
        test_dict = {'1': 1, '2': 2, '3': 3}
        subs = Subscriber(
            sub,
            onSuccess={
                'func': on_success,
                'args': test_tuple,
                'kwargs': test_dict
            }
        )
        sleep(NEXT_WAIT)

        self.assertEqual(test_val, 'init_val')
        self.assertTupleEqual(test_tuple, test_args)
        self.assertDictEqual(test_dict, test_kwargs)

        subs.success('new')

        self.assertEqual(test_val, 'new')
        self.assertTupleEqual(test_tuple, test_args)
        self.assertDictEqual(test_dict, test_kwargs)

    def test_error_1(self):
        """
        """
        sub = Subject('TestSubscriberSuite_test_error_1', initial_value='init_val')
        test_val = False
        def on_error(error):
            nonlocal test_val
            test_val = error

        self.assertEqual(test_val, False)
        subs = Subscriber(sub, onSuccess=lambda value: None, onError=on_error)

        subs.error('new')
        self.assertEqual(test_val, 'new')

    def test_error_2(self):
        """
        """
        sub = Subject('TestSubscriberSuite_test_error_2', initial_value='init_val')
        test_args = None
        test_val = False
        test_kwargs = None
        def on_error(*args, error=None, **kwargs):
            nonlocal test_val, test_args, test_kwargs
            test_args = args
            test_val = error
            test_kwargs = kwargs

        self.assertEqual(test_val, False)
        test_tuple = (1, 2, 3)
        test_dict = {'1': 1, '2': 2, '3': 3}
        subs = Subscriber(
            sub,
            onSuccess=lambda value: None,
            onError={
                'func': on_error,
                'args': test_tuple,
                'kwargs': test_dict
            }
        )
        sleep(NEXT_WAIT)

        subs.error('new')

        self.assertEqual(test_val, 'new')
        self.assertTupleEqual(test_tuple, test_args)
        self.assertDictEqual(test_dict, test_kwargs)

    def test_unsubscribe(self):
        """
        """
        sub = Subject('TestSubscriberSuite_test_unsubscribe', initial_value='init_val')
        test_val = False
        def on_success(value):
            nonlocal test_val
            test_val = value

        self.assertEqual(test_val, False)
        subs = Subscriber(sub, onSuccess=on_success)
        self.assertEqual(test_val, 'init_val')

        sub.next('new')
        sleep(NEXT_WAIT)
        self.assertEqual(test_val, 'new')

        subs.unsubscribe()

        sub.next('new1')
        sleep(NEXT_WAIT)
        self.assertEqual(test_val, 'new')
