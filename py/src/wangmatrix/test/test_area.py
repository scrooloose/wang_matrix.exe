import unittest
from unittest import mock
from wangmatrix.partition import *

class TestArea(unittest.TestCase):
    def test_r_is_set(self):
        self.assertEqual(Area(x=5, w=10).r, 14)

    def test_b_is_set(self):
        self.assertEqual(Area(y=5, h=10).b, 14)

    def test_mid_y(self):
        self.assertEqual(Area(y=10, h=10).mid_y(), 15)

    def test_mid_x(self):
        self.assertEqual(Area(x=10, w=10).mid_x(), 15)

    def test_y_overlap_with(self):
        a1 = Area(y=10, h=5)
        a2 = Area(y=11, h=50)
        self.assertEqual(a1.y_overlap_with(a2), [12, 13])

    def test_x_overlap_with(self):
        a1 = Area(x=10, w=5)
        a2 = Area(x=11, w=50)
        self.assertEqual(a1.x_overlap_with(a2), [12, 13])

    def test_scale_delegates_to_scalers(self):
        h_s = Scaler()
        w_s = Scaler()
        h_s.perform = mock.MagicMock(return_value=1)
        w_s.perform = mock.MagicMock(return_value=1)

        Area(w=10, h=5).scale(h_scaler=h_s, w_scaler=w_s)
        h_s.perform.assert_called_with(5)
        w_s.perform.assert_called_with(10)


    def test_scale_returns_a_new_area(self):
        assert isinstance(Area().scale(h_scaler=Scaler(), w_scaler=Scaler()), Area)
