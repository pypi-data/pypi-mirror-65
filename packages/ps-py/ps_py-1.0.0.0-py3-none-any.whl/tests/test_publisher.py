#! /usr/bin/env python3
"""This module tests the publisher's functionality
"""


# __all__ = []
__version__ = '1.0.0.0'
__author__ = 'Midhun C Nair <midhunch@gmail.com>'
__maintainers__ = [
    'Midhun C Nair <midhunch@gmail.com>',
]


import unittest

from time import sleep

from ps_py.publisher import Publisher


class TestPublisherSuite(unittest.TestCase):
    """
    """
    def test_singleton(self):
        """
        """
        pub1 = Publisher()
        pub2 = Publisher()
        pub3 = Publisher()

        self.assertEqual(id(pub1), id(pub2))
        self.assertEqual(id(pub3), id(pub2))
        self.assertEqual(id(pub1), id(pub3))

    def test_initialize(self):
        """
        """
        pub1 = Publisher()
        pub2 = Publisher(subject='TestPublisherSuite_test_initialize', kwargs={'initial_value':'test_value'})
        self.assertTrue('TestPublisherSuite_test_initialize' in pub1.subjects)
        self.assertTrue('TestPublisherSuite_test_initialize' in pub2.subjects)

    def test_different_subject_addition(self):
        """
        """
        pub = Publisher()
        subject = pub.get_subject('TestPublisherSuite_test_different_subject_addition')
        self.assertTrue('TestPublisherSuite_test_different_subject_addition' in pub.subjects)
        subject2 = pub.add('TestPublisherSuite_test_different_subject_addition', initial_value=None)
        self.assertEqual(id(subject), id(subject2))

    def test_subject_addition_callable(self):
        """
        """
        pub = Publisher()
        subject = pub.add(lambda x,y,z=None: (x, y, z), 'x', 'y', z='z')
        name = subject.name
        self.assertTrue(name in pub.subjects)

    def test_subject_addition(self):
        """
        """
        pub = Publisher()
        subject = pub.add('TestPublisherSuite_test_subject_addition', initial_value='test_val')
        self.assertEqual(subject.value, 'test_val')

    def test_subscribe(self):
        """
        """
        pub = Publisher()
        test_var = False
        def on_success(value):
            nonlocal test_var
            test_var = value

        self.assertEqual(test_var, False)
        pub.get_subject('test_subscribe')
        pub.subscribe('test_subscribe', onSuccess=on_success)
        self.assertEqual(test_var, False)
        pub.next('test_subscribe', True)
        sleep(.1)
        self.assertEqual(test_var, True)

    def test_next(self):
        """
        """
        pub = Publisher()
        test_var1 = False
        def on_success1(value):
            nonlocal test_var1
            test_var1 = value

        test_var2 = False
        def on_success2(value):
            nonlocal test_var2
            test_var2 = value

        # base for subject = test_next1
        self.assertEqual(test_var1, False)
        pub.get_subject('TestPublisherSuite_test_next1')
        pub.subscribe('TestPublisherSuite_test_next1', onSuccess=on_success1)
        self.assertEqual(test_var1, False)
        pub.next('TestPublisherSuite_test_next1', True)
        sleep(.1)
        self.assertEqual(test_var1, True)

        # base for subject = test_next2
        self.assertEqual(test_var2, False)
        pub.get_subject('TestPublisherSuite_test_next2')
        pub.subscribe('TestPublisherSuite_test_next2', onSuccess=on_success2)
        self.assertEqual(test_var2, False)
        pub.next('TestPublisherSuite_test_next2', True)
        sleep(.1)
        self.assertEqual(test_var2, True)

        # cross test by changing subject test_next1
        pub.next('TestPublisherSuite_test_next1', 'new_val')
        sleep(.1)
        self.assertEqual(test_var1, 'new_val')  # value should change
        self.assertEqual(test_var2, True)  # should be last value.

        # cross test by changing subject test_next2
        pub.next('TestPublisherSuite_test_next2', 'new_val2')
        sleep(.1)
        self.assertEqual(test_var1, 'new_val')  # shold be last value.
        self.assertEqual(test_var2, 'new_val2')  # value should change

    def test_subject_property(self):
        """
        """
        pub = Publisher()
        self.assertTrue(isinstance(pub.subjects, dict))
        pub.get_subject('TestPublisherSuite_test_subject_property')
        self.assertTrue(isinstance(pub.subjects, dict))
        self.assertTrue('TestPublisherSuite_test_subject_property' in pub.subjects)
        pub.get_subject('TestPublisherSuite_test_subject_property1')
        self.assertTrue(isinstance(pub.subjects, dict))
        self.assertTrue('TestPublisherSuite_test_subject_property' in pub.subjects)
        self.assertTrue('TestPublisherSuite_test_subject_property1' in pub.subjects)
