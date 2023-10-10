import unittest


# Example function to be tested
def add(a, b):
    return a + b


# Define a test case class that inherits from unittest.TestCase
class TestAddition(unittest.TestCase):

    # Test case to check if addition works correctly
    def test_addition(self):
        self.assertEqual(add(2, 3), 5)  # Assert that 2 + 3 = 5

    # Test case to check if addition works with negative numbers
    def test_addition_with_negatives(self):
        self.assertEqual(add(-2, 3), 1)  # Assert that -2 + 3 = 1

    # Test case to check if addition works with zero
    def test_addition_with_zero(self):
        self.assertEqual(add(0, 5), 5)  # Assert that 0 + 5 = 5
        self.assertEqual(True, False)


# Define a test suite
def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(TestAddition('test_addition'))
    suite.addTest(TestAddition('test_addition_with_negatives'))
    suite.addTest(TestAddition('test_addition_with_zero'))
    return suite


if __name__ == '__main__':
    # Run the tests
    runner = unittest.TextTestRunner()
    runner.run(test_suite())
