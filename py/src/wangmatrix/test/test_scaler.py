import unittest
from wangmatrix.partition import *

class TestScaler(unittest.TestCase):
    def test_scaler_respects_min_val(self):
        self.assertEqual(Scaler(min_perc=1, max_perc=2, min_val=100).perform(1000), 100)

    def test_scaler_respects_max_perc(self):
        def max_rand(lo, hi): return hi

        self.assertEqual(Scaler(min_perc=10, max_perc=50).perform(100, randfunc=max_rand), 50)

    def test_scaler_respects_min_perc(self):
        def min_rand(lo, hi): return lo

        self.assertEqual(Scaler(min_perc=10, max_perc=50).perform(100, randfunc=min_rand), 10)
