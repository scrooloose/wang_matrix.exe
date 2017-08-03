from unittest import TestCase

from hypothesis import given, strategies as st
from zope.interface.verify import verifyObject

from wangmatrix.drawing import (
    IShape, Circle, Square, Triangle, Vector, Canvas, Pixel, decorate
)


def triangles():
    return st.builds(
        Triangle,
        x=st.integers(0, 100),
        y=st.integers(0, 100),
        length=st.integers(1, 100),
        angle=st.integers(),
        rotation=st.integers(),
    )


def vectors():
    return st.builds(
        Vector,
        x=st.integers(0, 100),
        y=st.integers(0, 100),
        length=st.integers(1, 100),
        angle=st.integers(),
    )


def squares():
    return st.builds(
        Square,
        x=st.integers(0, 100),
        y=st.integers(0, 100),
        width=st.integers(1, 100),
        height=st.integers(1, 100),
    )


def circles():
    return st.builds(
        Circle,
        x=st.integers(0, 100),
        y=st.integers(0, 100),
        radius=st.integers(1, 100),
    )


def print_shape(shape):
    c = Canvas(20, 20, background=" ")
    c.draw(Pixel(p, ".") for p in shape.outline())
    return "\n" + decorate(c)


def make_ishape_tests(shape_strategy):
    class Tests(TestCase):
        @given(shape_strategy)
        def test_interface(self, shape):
            self.assertTrue(verifyObject(IShape, shape))

        @given(shape_strategy)
        def test_origin(self, shape):
            """
            The outline of the shape touches the origin.
            """
            min_x = min(p.x for p in shape.outline())
            min_y = min(p.y for p in shape.outline())
            self.assertEqual(shape.x, min_x, print_shape(shape))
            self.assertEqual(shape.y, min_y, print_shape(shape))

    return Tests


class CircleTests(make_ishape_tests(circles())):
    pass


class SquareTests(make_ishape_tests(squares())):
    pass


class TriangleTests(make_ishape_tests(triangles())):
    pass


class VectorTests(make_ishape_tests(vectors())):
    pass
