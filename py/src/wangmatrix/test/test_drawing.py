from functools import partial
from unittest import TestCase

from hypothesis import given, strategies as st
from zope.interface.verify import verifyObject

from wangmatrix.drawing import IShape, Circle, Square, Triangle, Vector


class IShapeTestsMixin(object):
    def test_interface(self):
        self.assertTrue(verifyObject(IShape, self.shape()))

    @given(x=st.integers(), y=st.integers())
    def test_origin(self, x, y):
        """
        The outline of the shape touches the origin.
        """
        o = self.shape(x=x, y=y)
        min_x = min(p.x for p in o.outline())
        min_y = min(p.y for p in o.outline())
        self.assertEqual(x, min_x, o)
        self.assertEqual(y, min_y, o)


def make_ishape_tests(shape_factory):
    class Tests(IShapeTestsMixin, TestCase):
        def setUp(self):
            self.shape = shape_factory

    return Tests


class CircleTests(make_ishape_tests(partial(Circle, x=0, y=0, radius=10))):
    pass


class SquareTests(
    make_ishape_tests(partial(Square, x=0, y=0, width=10, height=10))
):
    pass


class TriangleTests(
    make_ishape_tests(partial(Triangle, x=0, y=0, length=10, angle=0))
):
    pass


class VectorTests(
    make_ishape_tests(partial(Vector, x=0, y=0, length=10, angle=0))
):
    pass
