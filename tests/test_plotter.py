import unittest
from datetime import datetime


class TestCurrencyPlot(unittest.TestCase):

    def test_generate_xticks(self):
        currency_plot = Plotter([1, 2, 3], [4, 5, 6])
        currency_plot.set_values([1, 2, 3], [3, 4, 5, 6])

        date_now = datetime(2023, 10, 10)
        expected_xticks = ['08-10', '09-10', '10-10', '11-10', '12-10', '13-10']

        result = currency_plot._Plotter__generate_xticks(date_now)
        self.assertEqual(expected_xticks, result)

    def test_generate_xticks_transition_months(self):
        currency_plot = Plotter([1, 2, 3], [4, 5, 6])
        currency_plot.set_values([1, 2, 3], [3, 4, 5, 6])

        date_now = datetime(2023, 10, 1)
        expected_xticks = ['29-09', '30-09', '01-10', '02-10', '03-10', '04-10']

        result = currency_plot._Plotter__generate_xticks(date_now)
        self.assertEqual(expected_xticks, result)

    def test_generate_xticks_without_second_list(self):
        currency_plot = Plotter([1, 2, 3], [])
        currency_plot.set_values([1, 2, 3], [3])

        date_now = datetime(2023, 10, 10)
        expected_xticks = ['08-10', '09-10', '10-10']

        result = currency_plot._Plotter__generate_xticks(date_now)
        self.assertEqual(expected_xticks, result)

    def test_generate_xticks_one_element_first_list(self):
        currency_plot = Plotter([1], [4, 5, 6])
        currency_plot.set_values([1], [1, 4, 5, 6])

        date_now = datetime(2023, 10, 10)
        expected_xticks = ['10-10', '11-10', '12-10', '13-10']

        result = currency_plot._Plotter__generate_xticks(date_now)
        self.assertEqual(expected_xticks, result)

    def test_generate_xticks_float_elements(self):
        currency_plot = Plotter([1.1, 2.1, 3.1], [4.1, 5.1, 6.1])
        currency_plot.set_values([1.1, 2.1, 3.1], [3.1, 4.1, 5.1, 6.1])

        date_now = datetime(2023, 10, 10)
        expected_xticks = ['08-10', '09-10', '10-10', '11-10', '12-10', '13-10']

        result = currency_plot._Plotter__generate_xticks(date_now)
        self.assertEqual(expected_xticks, result)
