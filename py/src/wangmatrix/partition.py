import random
import drawing

class Area(object):
    def __init__(self, x=0, y=0, w=1, h=1):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.r = x + w - 1
        self.b = y + h - 1

    def __repr__(self):
        return "Area[top-left: %d,%d. Bot right: %d,%d]" % (self.x, self.y, self.r, self.b)


class BSPPartitioner(object):

    def __init__(self, min_h=6, min_w=6):
        self.min_h = min_h
        self.min_w = min_w
        self.__areas = []

    def perform(self, area, cut="vertical"):
        self._perform_for_real(area, cut=cut)
        return self.__areas

    def _perform_for_real(self, area, cut=None):
        next_cut = "horizontal" if cut == "vertical" else "vertical"

        for child_area in getattr(self, "_cut_" + cut)(area=area):
            self._perform_for_real(child_area, cut=next_cut)

    def _cut_vertical(self, area):
        cut = self._cut_position(area.w-1, self.min_w)
        if cut == None:
            self.__areas.append(area)
            return []

        left = Area(x=area.x, y=area.y, w=cut, h=area.h)
        right = Area(left.r, y=area.y, w=area.w - cut + 1, h=area.h)
        return [left, right]

    def _cut_horizontal(self, area):
        cut = self._cut_position(area.h-1, self.min_h)

        if cut == None:
            self.__areas.append(area)
            return []

        top = Area(x=area.x, y=area.y, w=area.w, h=cut)
        bottom = Area(x=area.x, y=top.b, w=area.w, h=area.h - cut + 1)
        return [top, bottom]

    def _cut_position(self, width, smallest):
        buffer = smallest if smallest % 2 == 0 else smallest + 1
        if buffer * 2 >= width:
            return None
        return random.randint(0 + buffer, width - buffer)


def main(h=40, w=100):
    root_area = Area(x=1,y=1,h=h,w=w)
    canvas = drawing.Canvas(w+1, h+1)

    areas = BSPPartitioner(min_h=10, min_w=20).perform(root_area)

    for a in areas:
        square = drawing.Square(a.x, a.y, a.w, a.h)
        canvas.draw(drawing.Pixel(p, "#") for p in square.outline())

    print(str(drawing.decorate(canvas)))
