#! /usr/bin/env python3
"""This module tests the contrib functions' functionality
"""


__all__ = [
    'TestMergeSuite',
    'TestOfSuite',
    'TestMapClassSuite',
    'TestMapSuite',
]
__version__ = '1.0.0.1'
__author__ = 'Midhun C Nair <midhunch@gmail.com>'
__maintainers__ = [
    'Midhun C Nair <midhunch@gmail.com>',
]


import unittest
import threading

from time import (
    sleep,
    time,
)

from ps_py.contrib import (
    Merge,
    Of,
    Map as psMap,
    map as psmap,
)
from ps_py.subject import Subject

from .constants import (
    NEXT_WAIT,
)


class TestMergeSuite(unittest.TestCase):
    """
    """
    def test_merge_wrong_input_1(self):
        """
        """
        with self.assertRaises(ValueError):
            Merge("test")

    def test_merge_wrong_input_2(self):
        """
        """
        sub = Subject("TestMergeSuite_test_merge_wrong_input_2", 'init')
        merge = Merge(sub)
        with self.assertRaises(ValueError):
            merge.args = "test"

    def test_initialize_1(self):
        """
        """
        merge = Merge()
        self.assertTrue(hasattr(merge, 'id'))
        self.assertTrue(hasattr(merge, 'int_id'))
        self.assertTrue(hasattr(merge, 'subject'))

    def test_initialize_2(self):
        """
        """
        sub = Subject("TestMergeSuite_test_initialize_2", 'init')
        merge = Merge(sub)
        self.assertTrue(hasattr(merge, 'id'))
        self.assertTrue(hasattr(merge, 'int_id'))
        self.assertTrue(hasattr(merge, 'subject'))
        self.assertTupleEqual((sub,), merge.args)

    def test_merge_subscribe(self):
        """
        """
        sub1 = Subject("TestMergeSuite_test_merge_subscribe1", None)
        sub2 = Subject("TestMergeSuite_test_merge_subscribe2", None)

        merge = Merge(sub1, sub2)

        test_val = False
        def on_success(value):
            nonlocal test_val
            test_val = value

        self.assertEqual(test_val, False)
        merge.subscribe(onSuccess=on_success)
        self.assertEqual(test_val, False)

        sub1.next("sub1 - new")
        sleep(NEXT_WAIT)
        self.assertEqual(test_val, "sub1 - new")

        sub2.next("sub2 - new")
        sleep(NEXT_WAIT)
        self.assertEqual(test_val, "sub2 - new")

        sub1.next("sub1 - new1")
        sleep(NEXT_WAIT)
        self.assertEqual(test_val, "sub1 - new1")

        sub2.next("sub2 - new1")
        sleep(NEXT_WAIT)
        self.assertEqual(test_val, "sub2 - new1")

    def test_pipe(self):
        """
        """
        sub1 = Subject('TestMergeSuite_test_pipe_1', initial_value='val1')
        sub2 = Subject('TestMergeSuite_test_pipe_2', initial_value='val2')

        merge = Merge(sub1, sub2)

        t_val1 = []
        def on_success(value):
            nonlocal t_val1
            t_val1.append(value)

        def on_success_pipe1(value):
            return "%s:%s:123" % (value, 'what')

        def on_success_pipe2(value):
            return "%s:%s" % (value, 'why')

        self.assertListEqual(t_val1, [])
        merge.pipe(
            psmap(onSuccess=on_success_pipe1),
            psmap(onSuccess=on_success_pipe2),
        ).subscribe(onSuccess=on_success)

        sub1.next('new_val1')
        sleep(NEXT_WAIT)
        sub2.next('new_val2')
        sleep(NEXT_WAIT)

        self.assertListEqual(
            t_val1,
            [
                'val1:what:123:why',
                'val2:what:123:why',
                'new_val1:what:123:why',
                'new_val2:what:123:why',
            ]
        )


class TestOfSuite(unittest.TestCase):
    """
    """

    def test_of_wrong_input(self):
        """
        """
        of_obj = Of("test")
        with self.assertRaises(ValueError):
            of_obj.args = "test"

    def test_initialize_1(self):
        """
        """
        of_obj = Of()
        self.assertTrue(hasattr(of_obj, 'id'))
        self.assertTrue(hasattr(of_obj, 'int_id'))
        self.assertTrue(hasattr(of_obj, 'subject'))
        self.assertTrue(hasattr(of_obj, 'index'))
        self.assertTrue(hasattr(of_obj, 'timeout'))
        self.assertEqual(of_obj.index, -1)
        self.assertEqual(of_obj.timeout, 5)

    def test_initialize_2(self):
        """
        """
        of_obj = Of(1, timeout=10)
        self.assertTrue(hasattr(of_obj, 'id'))
        self.assertTrue(hasattr(of_obj, 'int_id'))
        self.assertTrue(hasattr(of_obj, 'subject'))
        self.assertTupleEqual((1,), of_obj.args)
        self.assertTrue(hasattr(of_obj, 'index'))
        self.assertTrue(hasattr(of_obj, 'timeout'))
        self.assertEqual(of_obj.index, -1)
        self.assertEqual(of_obj.timeout, 10)

    def test_subscibe(self):
        """
        """
        lock = threading.Lock()
        of_args = [1, [1,2,3], (1,2,3), {1,2,3}, {1:1, 2:2, 3:3}]
        timeout = 2
        of_obj = Of(*of_args, timeout=timeout)

        test_val1 = False
        prev_val1 = False
        def on_success1(value):
            nonlocal test_val1, prev_val1
            lock.acquire()
            prev_val1 = test_val1
            test_val1 = value
            lock.release()

        test_val2 = False
        prev_val2 = False
        def on_success2(value):
            nonlocal test_val2, prev_val2
            lock.acquire()
            prev_val2 = test_val2
            test_val2 = value
            lock.release()

        self.assertEqual(test_val1, False)
        of_obj.subscribe(onSuccess=on_success1)
        of_obj.subscribe(onSuccess=on_success2)
        sleep(NEXT_WAIT)
        self.assertEqual(test_val1, of_args[0])
        self.assertEqual(test_val2, of_args[0])
        sleep(timeout+NEXT_WAIT)
        self.assertEqual(test_val1, of_args[1])
        self.assertEqual(test_val2, of_args[1])


class TestMapClassSuite(unittest.TestCase):
    """
    """
    def test_initialize(self):
        """
        """
        success = lambda value: None
        error = lambda error: None
        map_obj = psMap(subject='TestMapClassSuite_test_initialize', success=success, error=error)
        self.assertTrue(hasattr(map_obj, 'subject'))
        self.assertTrue(hasattr(map_obj, 'initial_value'))
        self.assertTrue(hasattr(map_obj, 'value'))
        self.assertTrue(hasattr(map_obj, '_args'))
        self.assertTrue(hasattr(map_obj, '_kwargs'))
        self.assertTrue(hasattr(map_obj, 'index'))
        self.assertTrue(hasattr(map_obj, 'mapSub'))
        self.assertEqual(map_obj.index, -1)
        self.assertTupleEqual(map_obj._args, tuple())
        self.assertDictEqual(map_obj._kwargs, dict())
        self.assertFalse(map_obj.mapSub.name in map_obj.subscribers)

    def test_subscribe(self):
        """
        """
        sub = Subject('TestMapClassSuite_test_subscribe', initial_value='val1')
        def on_success_pipe1(value):
            return "%s:%s:123" % (value, 'what')

        error = lambda error: None

        test_val = False
        def on_success(value):
            nonlocal test_val
            test_val = value
        self.assertEqual(test_val, False)

        map_obj = psMap(
            subject='TestMapClassSuite_test_subscribe_map',
            success=on_success_pipe1,
            error=error
        )
        map_obj.subscribe(onSuccess=on_success)
        self.assertEqual(test_val, False)

        sub.pipe(map_obj)

        sub.next('val2')
        sleep(NEXT_WAIT)
        self.assertEqual(test_val, 'val2:what:123')

    def test_pipe(self):
        """
        """
        sub = Subject('TestMapClassSuite_test_pipe', initial_value='val1')
        def on_success_pipe1(value):
            return "%s:%s:123" % (value, 'what')

        def on_successpipe2(value):
            return "%s:%s" % (value, 'why')

        error = lambda error: print(error)

        test_val_1 = False
        def on_success_1(value):
            nonlocal test_val_1
            test_val_1 = value
        self.assertEqual(test_val_1, False)

        test_val_2 = False
        def on_success_2(value):
            nonlocal test_val_2
            test_val_2 = value
        self.assertEqual(test_val_2, False)

        map_obj_1 = psMap(
            subject='TestMapClassSuite_test_pipe_map_1',
            success=on_success_pipe1,
            error=error
        )
        map_obj_1.subscribe(onSuccess=on_success_1)
        map_obj_2 = psMap(
            subject='TestMapClassSuite_test_pipe_map_2',
            success=on_successpipe2,
            error=error
        )
        map_obj_2.subscribe(onSuccess=on_success_2)
        self.assertEqual(test_val_1, False)
        self.assertEqual(test_val_2, False)

        sub.pipe(map_obj_1)
        map_obj_1.pipe(map_obj_2)

        sub.next('val2')
        sleep(NEXT_WAIT)
        self.assertEqual(test_val_1, 'val2:what:123')
        self.assertEqual(test_val_2, 'val2:what:123:why')


class TestMapSuite(unittest.TestCase):
    """
    """
    def test_wrong_input_1(self):
        """
        """
        with self.assertRaises(ValueError):
            psmap("test")

    def test_wrong_input_2(self):
        """
        """
        with self.assertRaises(ValueError):
            psmap(lambda value: None, onError="test")

    def test_output_1(self):
        """
        """
        success = lambda value: None
        error = lambda error: None
        map_obj = psmap(success, error)
        self.assertTrue(isinstance(map_obj, psMap))

    def test_output_2(self):
        """
        """
        success = lambda value: None
        map_obj = psmap(success,)
        self.assertTrue(isinstance(map_obj, psMap))
        self.assertTrue(callable(map_obj.onError))
