import unittest
from unittest.mock import MagicMock, patch
from fastapi.exceptions import HTTPException

# Import the Server class
from src.app.app import Server


class TestServer(unittest.TestCase):
    def setUp(self):
        self.server = Server()

    def test_validate_currency_inputs(self):
        # Test case for valid currencies
        self.assertIsNone(self.server.validate_currency_inputs("USD", "EUR"))

        # Test case for the same currency
        with self.assertRaises(HTTPException):
            self.server.validate_currency_inputs("USD", "USD")

        # Test case for empty currency A
        with self.assertRaises(HTTPException):
            self.server.validate_currency_inputs("", "EUR")

        # Test case for empty currency B
        with self.assertRaises(HTTPException):
            self.server.validate_currency_inputs("USD", "")

    def test_generate_currency_plot(self):
        exchange_rate7days = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]
        extrapolated_exchange_rate = [8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0]

        plot = self.server.generate_currency_plot(exchange_rate7days, extrapolated_exchange_rate)

        # Ensure that the generated plot is not None
        self.assertIsNotNone(plot)

    def test_encode_graph(self):
        # Mock the graph
        self.server.graph = MagicMock()

        encoded = self.server.encode_graph()

        # Ensure that the encoded data is not None
        self.assertIsNotNone(encoded)



if __name__ == '__main__':
    unittest.main()
