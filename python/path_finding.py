from Queue import PriorityQueue


class PathFinder(object):
    def __init__(self, mapped_area, target, source):
        self.map = mapped_area
        self.target = Point(target[0], target[1])
        self.source = Point(source[0], source[1])

    def heuristic(self, a, b):
        return abs(a.x - b.x) + abs(a.y - b.y)

    def get_path(self):
        frontier = PriorityQueue()
        frontier.put(self.source, 0)
        came_from = {}
        cost_so_far = {}
        came_from[self.source] = None
        cost_so_far[self.source] = 0

        while not frontier.empty():
            current = frontier.get()

            for next in self.get_neighbors(current):
                new_cost = cost_so_far[current] + self.cost(current, next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(self.target, next)
                    frontier.put(next, priority)
                    came_from[next] = current

        # now reconstruct the path
        current = self.target
        path = [current]
        while current != self.source:
            print came_from
            print current
            print
            current = came_from[current]
            path.append(current)

        return path

    def get_neighbors(self, point):
        if self.map is not None or len(self.map) == 0:
            return []

        x_len = len(self.map)
        y_len = len(self.map[0])

        # there can be up to 4 neighbors (for now)
        up = Point(point.x, point.y + 1) if point.y + 1 < y_len else None
        down = Point(point.x, point.y - 1) if point.y - 1 >= 0 else None
        left = Point(point.x - 1, point.y) if point.x - 1 >= 0 else None
        right = Point(point.x + 1, point.y) if point.x + 1 < x_len else None

        all_points = [up, down, left, right]

        # only return points that are on the grid and that are passable
        return [p for p in all_points if p is not None and self.map[p.x][p.y] < 1]

    def cost(self, current, next):
        ### TODO: check if there is a danger of being shot here, and adjust accordingly
        return 1


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)
