import unittest

from src.predictor.predictor import Predictor


class TestPredictor(unittest.TestCase):
    def test_extrapolate_currency_rate(self):
        p = Predictor().extrapolate_currency_rate([1, 1.1])
        result = [1, 1.1, 1.2100000000000002, 1.3310000000000004, 1.4641000000000006, 1.6105100000000008, 1.771561000000001, 1.9487171000000014]
        self.assertEqual(p, result)

    def test_extrapolate_currency_rate2(self):
        p = Predictor().extrapolate_currency_rate([3, 4, 5])
        result = [3, 4, 5, 6.25, 7.8125, 9.765625, 12.20703125, 15.2587890625, 19.073486328125]
        self.assertEqual(p, result)

    def test_exchange_rate(self):
        p = Predictor().exchange_rate([1, 1.1], [10, 11], 3)
        result = 10.0
        self.assertEqual(p, result)

    def test_exchange_rate2(self):
        p = Predictor().exchange_rate([1, 2, 2.5], [11, 12], 3)
        result = 5.236363636363636
        self.assertEqual(p, result)
