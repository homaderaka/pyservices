import unittest

from src.plotter.plotter import Plotter


class TestDependency(unittest.TestCase):
    # Тест, чтобы проверить, не ломаются ли зависимости при импорте из src
    def test_plotter(self):
        p = Plotter([1, 2, 3], [4, 5, 6]).get_plot()
        self.assertIsNotNone(p)
