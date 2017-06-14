import random
import drawing

class BSPTree(object):
    def __init__(self, area, parent=None, left_child=None, right_child=None, cut=None):
        self.area = area
        self.left_child = left_child
        self.right_child = right_child
        self.cut = cut
        self.parent = parent

    #FIXME: should probably cache this or something
    def leaves(self):
        rv = []
        self.each_leaf(lambda l: rv.append(l))
        return rv

    def leaf_parents(self):
        return list(set(map(lambda l: l.parent, self.leaves())))

    def each_leaf(self, callback):
        if self.is_leaf():
            callback(self)
        else:
            self.left_child.each_leaf(callback)
            self.right_child.each_leaf(callback)

    def is_leaf(self):
        return (self.left_child, self.right_child) == (None, None)

    def is_horizontal_cut(self):
        return self.cut == BSPPartitioner.CUT_HORIZONTAL

    def set_area(self, area):
        self.area = area

    def first_leaf_parent(self):
        leaves = self.leaves()
        if len(leaves) > 0:
            return leaves[0]

    def top_most_room(self):
        return min(self.leaves(), key=lambda l: l.area.y)

    def bottom_most_room(self):
        return max(self.leaves(), key=lambda l: l.area.b)

    def left_most_room(self):
        return min(self.leaves(), key=lambda l: l.area.x)

    def right_most_room(self):
        return max(self.leaves(), key=lambda l: l.area.r)

class Area(object):
    def __init__(self, x=0, y=0, w=1, h=1):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.r = x + w - 1
        self.b = y + h - 1

    def __repr__(self):
        return "Area[x:%d y:%d w:%d h:%d]" % (self.x, self.y, self.w, self.h)

    def scale(self, min_percent=50, max_percent=70, min_h=4, min_w=5):
        new_w = Scaler(scalar=self.w, min_perc=min_percent, max_perc = max_percent, min_val = min_w).perform()
        new_h = Scaler(scalar=self.h, min_perc=min_percent, max_perc = max_percent, min_val = min_h).perform()
        new_x = ((self.x + self.x + self.w) / 2) - (new_w / 2)
        new_y = ((self.y + self.y + self.h) / 2) - (new_h / 2)
        return Area(x = int(new_x), y = int(new_y), w = int(round(new_w)), h = int(round(new_h)))

    def render_to_canvas(self, canvas, char="#"):
        s = drawing.Square(self.x, self.y, self.w, self.h)
        canvas.draw(drawing.Pixel(p, char) for p in s.outline())

    def mid_y(self):
        return int(self.y + self.h/2)

    def mid_x(self):
        return int(self.x + self.w/2)

    def y_overlap_with(self, area):
        return sorted(set(self._y_overlap_range()).intersection(area._y_overlap_range()))

    def _y_overlap_range(self):
        return range(self.y + 1, self.y + self.h -1)

    def x_overlap_with(self, area):
        return sorted(set(self._x_overlap_range()).intersection(area._x_overlap_range()))

    def _x_overlap_range(self):
        return range(self.x + 1, self.x + self.w -1)


class Scaler(object):
    def __init__(self, scalar, min_perc, max_perc, min_val):
        self.scalar = scalar
        self.min_perc = min_perc
        self.max_perc = max_perc
        self.min_val = min_val

    def perform(self):
        return random.randint(self._min_value(), self._max_value())

    def _min_value(self):
        return max(self.min_val, int(self.scalar * self.min_perc / 100))

    def _max_value(self):
        return max(self.min_val, int(self.scalar * (self.max_perc / 100)))

class BSPPartitioner(object):
    CUT_HORIZONTAL="horizontal"
    CUT_VERTICAL="vertical"

    def __init__(self, min_h=6, min_w=6):
        self.min_h = min_h
        self.min_w = min_w

    def perform(self, area, cut=CUT_VERTICAL):
        btree = BSPTree(area=area, cut=cut)
        self._perform_for_real(btree, cut=cut)
        return btree

    def _perform_for_real(self, btree, cut=None):
        next_cut = self.CUT_HORIZONTAL if cut == self.CUT_VERTICAL else self.CUT_VERTICAL

        child_areas = getattr(self, "_cut_" + cut)(area=btree.area)

        if len(child_areas) > 0:
            btree.left_child = BSPTree(area=child_areas[0], parent=btree, cut=next_cut)
            btree.right_child = BSPTree(area=child_areas[1], parent=btree, cut=next_cut)
            self._perform_for_real(btree.left_child, cut=next_cut)
            self._perform_for_real(btree.right_child, cut=next_cut)

    def _cut_vertical(self, area):
        cut = self._cut_position(area.w-1, self.min_w)
        if cut == None:
            return []

        left = Area(x=area.x, y=area.y, w=cut, h=area.h)
        right = Area(left.r, y=area.y, w=area.w - cut + 1, h=area.h)
        return [left, right]

    def _cut_horizontal(self, area):
        cut = self._cut_position(area.h-1, self.min_h)

        if cut == None:
            return []

        top = Area(x=area.x, y=area.y, w=area.w, h=cut)
        bottom = Area(x=area.x, y=top.b, w=area.w, h=area.h - cut + 1)
        return [top, bottom]

    def _cut_position(self, width, smallest):
        buffer = smallest if smallest % 2 == 0 else smallest + 1
        if buffer * 2 >= width:
            return None
        return random.randint(0 + buffer, width - buffer)

class Path:
    def __init__(self, area1, area2, points):
        self.area1 = area1
        self.area2 = area2
        self.points = points

class PathBuilder:
    def __init__(self, btree):
        self.btree = btree
        self.paths = []

    def perform(self):
        # for n in map(lambda n: n.parent, self.btree.leaf_parents()):
        for n in self.btree.leaf_parents():
            self._connect(n)

        return self.paths

    def _connect(self, node):
        if node.is_horizontal_cut():
            self.paths.append(self._v_path_for(node))
        else:
            self.paths.append(self._h_path_for(node))

        if node.parent:
            self._connect(node.parent)

    def _h_path_for(self, node):
        if node.left_child.area.x < node.right_child.area.x:
            left = node.left_child.right_most_room().area
            right = node.right_child.left_most_room().area
        else:
            left = node.right_child.right_most_room().area
            right = node.left_child.left_most_room().area

        overlap = left.y_overlap_with(right)
        if overlap:
            mid_y = overlap[int(len(overlap)/2)]
            path_points = self._h_elbow_for(left.r, mid_y, right.x, mid_y)
        else:
            path_points = self._h_elbow_for(left.r, left.mid_y(), right.x, right.mid_y())

        return Path(points=path_points, area1 = node.left_child, area2 = node.right_child)

    def _v_path_for(self, node):
        if node.left_child.area.y < node.right_child.area.y:
            top = node.left_child.bottom_most_room().area
            bottom = node.right_child.top_most_room().area
        else:
            top = node.right_child.bottom_most_room().area
            bottom = node.left_child.top_most_room().area

        overlap = top.x_overlap_with(bottom)
        if overlap:
            mid_x = overlap[int(len(overlap)/2)]
            path_points = self._v_elbow_for(mid_x, top.b, mid_x, bottom.y)
        else:
            path_points = self._v_elbow_for(top.mid_x(), top.b, bottom.mid_x(), bottom.y)

        return Path(points=path_points, area1 = node.left_child, area2 = node.right_child)

    def _v_elbow_for(self, tx, ty, bx, by):
        half_y = int((by - ty) / 2)

        rv = []
        #top vertical bit
        for y in range(ty, ty + half_y):
            rv.append((tx, y))

        #horizontal middle bit
        for x in range(tx, bx, 1 if bx > tx else -1):
            rv.append((x, ty + half_y))

        #bottom vertical bit
        for y in range(ty + half_y, by+1):
            rv.append((bx, y))

        return rv

    def _h_elbow_for(self, lx, ly, rx, ry):
        half_x = int((rx - lx) / 2)

        rv = []
        #left horizontal bit
        for x in range(lx, lx + half_x):
            rv.append((x, ly))

        #vertical middle bit
        for y in range(ly, ry, 1 if ry > ly else -1):
            rv.append((lx + half_x, y))

        #right horizontal bit
        for x in range(lx + half_x, rx+1):
            rv.append((x, ry))

        return rv

def main(h=40, w=100, min_w=15, min_h=12, min_scale=40, max_scale=70):
    root_area = Area(x=1,y=1,h=h,w=w)
    canvas = drawing.Canvas(w+1, h+1)

    btree = BSPPartitioner(min_h=min_h, min_w=min_w).perform(root_area)

    btree.each_leaf(lambda node: (
        # node.area.render_to_canvas(canvas, char="."),
        node.set_area(node.area.scale(min_percent=min_scale, max_percent=max_scale)),
        node.area.render_to_canvas(canvas)))

    for path in PathBuilder(btree).perform():
        points = map(lambda p: drawing.Point(p[0], p[1]), path.points)
        pixels = map(lambda p: drawing.Pixel(p, "*"), points)
        canvas.draw(pixels)


    print(str(drawing.decorate(canvas)))

    return btree
