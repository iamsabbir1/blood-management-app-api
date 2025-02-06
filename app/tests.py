"""Sample tests"""

from django.test import SimpleTestCase
from app import calc


class CalcTests(SimpleTestCase):
    """Test the calculator module"""

    def test_add_numbers(self):
        """Test adding numbers together."""
        res = calc.add(5, 4)
        self.assertEqual(res, 9)

    def test_subtract_numbers(self):
        """Test subtracting two numbers"""

        res = calc.subtract(10, 5)
        self.assertEqual(res, 5)
