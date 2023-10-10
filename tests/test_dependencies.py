import unittest

from src.plotter.plotter import Plotter


class TestDependency(unittest.TestCase):

    def test_plotter(self):
        p = Plotter([1, 2, 3], [4, 5, 6])
        assert self.assertIsNotNone(p)