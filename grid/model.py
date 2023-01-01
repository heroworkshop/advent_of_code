import threading


class Grid:
    BOUNDARY = 1

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self._values = {}
        self.lock = threading.RLock()

    def value(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            with self.lock:
                return self._values.get((x, y), 0)
        return self.BOUNDARY

    def fill_cell(self, x, y, value):
        with self.lock:
            self._values[(x, y)] = value

    def clear(self):
        with self.lock:
            self._values.clear()

    def __iter__(self):
        return iter(self._values.items())

    def __contains__(self, v):
        return v in self._values

    def __len__(self):
        return len(self._values)
