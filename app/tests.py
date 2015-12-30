"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

# Integration test (with db)
from django.test import TestCase

# Unit test (without db)
from django.test import SimpleTestCase

class SimpleTest(SimpleTestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

    def test_basic_addition2(self):
        """
        Tests that 2 * 2 always equals 4.
        """
        self.assertEqual(2 * 2, 4)
