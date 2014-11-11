from Queue import PriorityQueue


class PathFinder(object):
    def __init__(self, mapped_area, target, source):
        self.map = mapped_area
        self.target = Point(int(target[0]), int(target[1]))
        self.source = Point(int(source[0]), int(source[1]))

    def heuristic(self, a, b):
        return abs(a.x - b.x) + abs(a.y - b.y)

    def get_path(self):
        if self.map is None or len(self.map) == 0:
            return []

        frontier = PriorityQueue()
        frontier.put((0 ,self.source,))
        came_from = {}
        cost_so_far = {}
        came_from[self.source] = None
        cost_so_far[self.source] = 0

        iteration_number = 0
        while not frontier.empty():
            iteration_number = iteration_number + 1
            current = frontier.get()[1]

            if abs(current.x - self.target.x) <= 2 and abs(current.y - self.target.y) <= 2:
                break

            if iteration_number == 20000:
                # give up and do something random
                print "REACHED MAX ITERATION NUMBER"
                break

            for next in self.get_neighbors(current):
                new_cost = cost_so_far[current] + self.cost(current, next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(self.target, next)
                    frontier.put((priority, next,))
                    came_from[next] = current

        # now reconstruct the path
        secondary_current = current
        current = self.target
        try:
            came_from[current]
        except KeyError:
            current = secondary_current

        path = [current]
        while current != self.source:
            current = came_from[current]
            path.append(current)

        path.reverse()

        for idx, node in enumerate(path):
            print "Node: " + str(idx) + " (" + str(node.x) + ", " + str(node.y) + ")"

        print "target: (" + str(self.target.x) + ", " + str(self.target.y) + ")"
        
        
        return path


    def get_neighbors(self, point):
        if self.map is None or len(self.map) == 0:
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
        self.x = int(x)
        self.y = int(y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)
