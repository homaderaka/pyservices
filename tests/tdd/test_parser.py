import datetime
import unittest

from src.parser.parser import Parser


class TestParser(unittest.TestCase):
    def test_parse_rub_for_usd_exchange_rate(self):
        parser = Parser()
        result = parser.getExchangeRate('USD', 'RUB', '10.10.2023')
        expected = 101.3598
        self.assertEqual(expected, result)


    def test_parse_usd_for_rub_exchange_rate(self):
        parser = Parser()
        result = parser.getExchangeRate('RUB', 'USD', '10.10.2023')
        expected = 0.009865844249889994
        self.assertEqual(expected, result)


    def test_parse_same_currency(self):
        parser = Parser()
        result = parser.getExchangeRate('RUB', 'RUB', '10.10.2023')
        expected = 1
        self.assertEqual(expected, result)


    def test_parse_datetime_partly_successfully(self):
        parser = Parser()
        result = parser.parseDate(datetime.datetime(2023,10,10))
        expected = "10.10.2023"
        self.assertEqual(expected, result)


    def test_parse_datetime_full_successfully(self):
        parser = Parser()
        result = parser.parseDate(datetime.datetime(2023,10,10,10,10,10))
        expected = "10.10.2023"
        self.assertEqual(expected, result)