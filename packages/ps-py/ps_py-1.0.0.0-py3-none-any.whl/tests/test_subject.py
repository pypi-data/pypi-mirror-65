#! /usr/bin/env python3
"""This module tests the subjects's functionality
"""


__all__ = [
    'TestSubjectSuite',
]
__version__ = '1.0.0.0'
__author__ = 'Midhun C Nair <midhunch@gmail.com>'
__maintainers__ = [
    'Midhun C Nair <midhunch@gmail.com>',
]


import unittest

from time import sleep

from ps_py.subject import Subject
from ps_py.contrib import (
    map as psmap,
)
from ps_py.subscriber import Subscriber

from .constants import (
    NEXT_WAIT,
    ASYNC_TIME,
)


class TestSubjectSuite(unittest.TestCase):
    """
    """
    def test_initialize_same_subject(self):
        """
        """
        sub1 = Subject('TestSubjectSuite_test_initialize', initial_value='val1')
        sub1.subscribe(onSuccess=lambda value: None, onError=lambda error: None)
        sub2 = Subject('TestSubjectSuite_test_initialize', initial_value='val2')
        self.assertEqual(id(sub1), id(sub2))
        self.assertNotEqual(sub1.value, 'val1')
        self.assertEqual(sub1.value, 'val2')
        self.assertEqual(sub2.value, 'val2')
        self.assertDictEqual(sub1.subscribers, sub2.subscribers)
        self.assertEqual(id(sub1.subscribers), id(sub2.subscribers))

    def test_initialize_publisher_singleton(self):
        """
        """
        sub1 = Subject('TestSubjectSuite_test_initialize_publisher_singleton', initial_value='val1')
        sub2 = Subject('TestSubjectSuite_test_initialize_publisher_singleton1', initial_value='val1')
        self.assertEqual(id(sub1.publisher), id(sub2.publisher))

    def test_initialize_string_sub(self):
        """
        """
        sub = Subject('TestSubjectSuite_test_initialize')
        self.assertTrue(hasattr(sub, 'subject'))
        self.assertTrue(hasattr(sub, 'initial_value'))
        self.assertTrue(hasattr(sub, 'value'))
        self.assertTrue(hasattr(sub, '_args'))
        self.assertTrue(hasattr(sub, '_kwargs'))
        self.assertTrue(hasattr(sub, 'index'))
        self.assertTrue(hasattr(sub, 'name'))
        self.assertEqual(sub.index, -1)
        self.assertEqual(sub.name, 'TestSubjectSuite_test_initialize')
        self.assertTupleEqual(sub._args, tuple())
        self.assertDictEqual(sub._kwargs, dict())

    def test_initialize_callable_sub(self):
        """
        """
        sub = Subject(lambda x=None: None)
        self.assertTrue(hasattr(sub, 'subject'))
        self.assertTrue(hasattr(sub, 'initial_value'))
        self.assertTrue(hasattr(sub, 'value'))
        self.assertTrue(hasattr(sub, '_args'))
        self.assertTrue(hasattr(sub, '_kwargs'))
        self.assertTrue(hasattr(sub, 'index'))
        self.assertEqual(sub.index, -1)
        self.assertTupleEqual(sub._args, tuple())
        self.assertDictEqual(sub._kwargs, dict())

    def test_subscribe(self):
        """
        """
        sub = Subject('TestSubjectSuite_test_subscribe', initial_value='val1')
        test_val = False
        def on_success(value):
            nonlocal test_val
            test_val = value

        self.assertEqual(test_val, False)
        sub.subscribe(onSuccess=on_success)
        self.assertEqual(test_val, 'val1')
        sub.next('val2')
        sleep(NEXT_WAIT)
        self.assertEqual(test_val, 'val2')

    def test_pipe(self):
        """
        """
        sub = Subject('TestSubjectSuite_test_pipe', initial_value='val1')

        t_val1 = False
        def on_success(value):
            nonlocal t_val1
            t_val1 = value

        def on_success_pipe1(value):
            return "%s:%s:123" % (value, 'what')

        def on_successpipe2(value):
            return "%s:%s" % (value, 'why')

        self.assertEqual(t_val1, False)
        sub.pipe(
            psmap(onSuccess=on_success_pipe1),
            psmap(onSuccess=on_successpipe2),
        ).subscribe(onSuccess=on_success)

        sub.next('val2')
        sleep(NEXT_WAIT*2)
        self.assertEqual(t_val1, 'val2:what:123:why')

    def test_next(self):
        """
        """
        sub = Subject('TestSubjectSuite_test_next', initial_value='val1')
        t_val1 = False
        def on_success1(value):
            nonlocal t_val1
            t_val1 = value

        t_val2 = False
        def on_success2(value):
            nonlocal t_val2
            t_val2 = value

        self.assertEqual(t_val1, False)
        self.assertEqual(t_val2, False)
        sub.subscribe(onSuccess=on_success1)
        sub.subscribe(onSuccess=on_success2)
        self.assertEqual(t_val1, 'val1')
        self.assertEqual(t_val2, 'val1')

        sub.next('val2')
        sleep(NEXT_WAIT)
        self.assertEqual(t_val1, 'val2')
        self.assertEqual(t_val2, 'val2')

        sub.next([1, 2, 3])
        sleep(NEXT_WAIT)
        self.assertEqual(t_val1, [1, 2, 3])
        self.assertEqual(t_val2, [1, 2, 3])

        sub.next({1, 2, 3})
        sleep(NEXT_WAIT)
        self.assertEqual(t_val1, {1, 2, 3})
        self.assertEqual(t_val2, {1, 2, 3})

        sub.next((1, 2, 3))
        sleep(NEXT_WAIT)
        self.assertEqual(t_val1, (1, 2, 3))
        self.assertEqual(t_val2, (1, 2, 3))

        sub.next({1: 1, 2: 2, 3: 3})
        sleep(NEXT_WAIT)
        self.assertEqual(t_val1, {1: 1, 2: 2, 3: 3})
        self.assertEqual(t_val2, {1: 1, 2: 2, 3: 3})

    def test_next_async(self):
        """
        """
        sub = Subject('TestSubjectSuite_test_next_async', initial_value='val1')
        t_val1 = False
        def on_success1(value):
            nonlocal t_val1
            sleep(ASYNC_TIME)
            t_val1 = value

        t_val2 = False
        def on_success2(value):
            nonlocal t_val2
            sleep(ASYNC_TIME)
            t_val2 = value

        self.assertEqual(t_val1, False)
        self.assertEqual(t_val2, False)
        sub.subscribe(onSuccess=on_success1)
        sub.subscribe(onSuccess=on_success2)
        sleep(NEXT_WAIT)
        self.assertEqual(t_val1, False)
        self.assertEqual(t_val2, False)
        sleep(ASYNC_TIME)
        self.assertEqual(t_val1, 'val1')
        self.assertEqual(t_val2, 'val1')
        sub.next('val2')
        sleep(NEXT_WAIT)
        self.assertEqual(t_val1, 'val1')
        self.assertEqual(t_val2, 'val1')
        sleep(ASYNC_TIME)
        self.assertEqual(t_val1, 'val2')
        self.assertEqual(t_val2, 'val2')

    def test_unsubscribe(self):
        """
        """
        sub = Subject('TestSubjectSuite_test_unsubscribe', initial_value='val1')
        t_val1 = False
        def on_success1(value):
            nonlocal t_val1
            t_val1 = value

        t_val2 = False
        def on_success2(value):
            nonlocal t_val2
            t_val2 = value

        self.assertEqual(t_val1, False)
        self.assertEqual(t_val2, False)
        sub.subscribe(onSuccess=on_success1)
        subs = sub.subscribe(onSuccess=on_success2)
        self.assertEqual(t_val1, 'val1')
        self.assertEqual(t_val2, 'val1')

        sub.unsubscribe(subs)

        sub.next('val2')
        sleep(NEXT_WAIT)
        self.assertEqual(t_val1, 'val2')
        self.assertEqual(t_val2, 'val1')

        sub.next([1, 2, 3])
        sleep(NEXT_WAIT)
        self.assertEqual(t_val1, [1, 2, 3])
        self.assertEqual(t_val2, 'val1')

    def test_add_subscriber(self):
        """
        """
        sub = Subject('TestSubjectSuite_test_add_subscriber', initial_value='val1')
        sub2 = Subject('TestSubjectSuite_test_add_subscriber_1', initial_value='val1')
        subs = Subscriber(sub, onSuccess=lambda value: None)

        self.assertTrue(subs.name in sub.subscribers)
        self.assertFalse(subs.name in sub2.subscribers)
        self.assertNotEqual(id(subs.subject), id(sub2))
        self.assertEqual(id(subs.subject), id(sub))

        sub2.add_subscriber(subs)

        self.assertTrue(subs.name in sub2.subscribers)
        self.assertNotEqual(id(subs.subject), id(sub))
        self.assertEqual(id(subs.subject), id(sub2))

    def test_add_subscriber_wrong_type(self):
        """
        """
        sub = Subject('TestSubjectSuite_test_add_subscriber_wrong_type', initial_value='val1')
        with self.assertRaises(ValueError):
            sub.add_subscriber("test")

    def test_sub_callable_subscribe_async_n_output(self):
        """
        """
        test_args = (1, 2, 3)
        test_kwargs = {'1': 1, '2': 2}
        test_output = False
        def callable_subject(*args, **kwargs):
            """
            """
            sleep(2*ASYNC_TIME)
            return args, kwargs

        def on_success(value):
            nonlocal test_output
            test_output = value

        self.assertEqual(test_output, False)
        sub = Subject(callable_subject, *test_args, **test_kwargs)
        sub.subscribe(onSuccess=on_success)
        self.assertEqual(test_output, False)
        sleep(2*ASYNC_TIME + NEXT_WAIT)
        self.assertTupleEqual(test_output[0], test_args)
        self.assertDictEqual(test_output[1], test_kwargs)
