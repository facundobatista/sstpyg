class SafeMap:

    # deltas
    DELTA_RIGHT = (1, 0)
    DELTA_LEFT = (-1, 0)
    DELTA_UP = (0, -1)
    DELTA_DOWN = (0, 1)
    ALL_DELTAS = [DELTA_DOWN, DELTA_RIGHT, DELTA_UP, DELTA_LEFT]
    _MARK = object()

    def __init__(self, max_x, max_y, out_of_map=_MARK, fill=None):
        self.max_x = max_x
        self.max_y = max_y
        self.xmap = [[fill] * max_x for _ in range(max_y)]
        if out_of_map is self._MARK:
            def _f():
                raise ValueError("out of map")
            self.out_of_map = _f
        else:
            self.out_of_map = lambda: out_of_map

    def __getitem__(self, coord):
        x, y = coord
        if (0 <= x < self.max_x) and (0 <= y < self.max_y):
            val = self.xmap[y][x]
        else:
            val = self.out_of_map()

        return val

    def __setitem__(self, coord, value):
        x, y = coord
        if (0 <= x < self.max_x) and (0 <= y < self.max_y):
            self.xmap[y][x] = value
        else:
            raise ValueError("out of map")

    def switch(self, coord, delta):
        """Switch the element from the coordinate with the coordinate + delta."""
        x1, y1 = coord
        dx, dy = delta
        x2 = x1 + dx
        y2 = y1 + dy
        self.xmap[y1][x1], self.xmap[y2][x2] = self.xmap[y2][x2], self.xmap[y1][x1]
        return (x2, y2)

    def show(self):
        """Show the map."""
        for row in self.xmap:
            print(" ".join(item for item in row))

    def find(self, to_find):
        """Return the first ocurrence of item."""
        for y, row in enumerate(self.xmap):
            for x, item in enumerate(row):
                if item == to_find:
                    return x, y
        raise ValueError("Couldn't find " + repr(to_find))

    def walk(self):
        """Walk through the map, yielding elements."""
        for row in self.xmap:
            for item in row:
                yield item
