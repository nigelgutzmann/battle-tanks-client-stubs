"""from Queue import PriorityQueue
import math


class PathFinder(object):
    def __init__(self, mapped_area, target, source, projectile_list):
        self.map = mapped_area
        self.target = Point(target[0], target[1])
        self.source = Point(source[0], source[1])
        self.projectile_list = projectile_list

    def heuristic(self, a, b):
        return abs(a.x - b.x) + abs(a.y - b.y)

    def get_path(self):
        if self.map is None or len(self.map) == 0:
            return []

        frontier = PriorityQueue()
        frontier.put((0, self.source,))
        came_from = {}
        cost_so_far = {}
        came_from[self.source] = None
        cost_so_far[self.source] = 0

        iteration_number = 0
        while not frontier.empty():
            iteration_number = iteration_number + 1
            current = frontier.get()[1]

            if abs(current.x - self.target.x) == 0 and abs(current.y - self.target.y) == 0:
                print "FOUND TARGET"
                break

            for next in self.get_neighbors(current):
                new_cost = cost_so_far[current] + self.cost(current, next, None)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(self.target, next)
                    frontier.put((priority, next,))
                    came_from[next] = current

        if frontier.empty():
            print "SCANNED EVERYWHERE"
            # choose somewhere far to go
        else:
            # choose somewhere we can go
            current = self.target

        path = [current]
        while current != self.source:
            current = came_from[current]
            path.append(current)

        path.reverse()

        #for idx, node in enumerate(path):
        #    print "Node: " + str(idx) + " (" + str(node.x) + ", " + str(node.y) + ")"
        #print "target: (" + str(self.target.x) + ", " + str(self.target.y) + ")

        return path

    '''def get_path(self):
        if self.map is None or len(self.map) == 0:
            return []

        frontier = PriorityQueue()
        frontier.put((0, self.source,))
        came_from = {}
        cost_so_far = {}
        length_so_far = {}
        came_from[self.source] = None
        cost_so_far[self.source] = 0
        length_so_far[self.source] = 0

        while not frontier.empty():
            current = frontier.get()[1]

            if abs(current.x - self.target.x) == 0 and abs(current.y - self.target.y) == 0:
                print "FOUND TARGET"
                break

            for next in self.get_neighbors(current):
                new_length = length_so_far[current] + 1
                new_cost = cost_so_far[current] + 1#self.cost(current, next, length_so_far[current])
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    length_so_far[next] = new_length
                    priority = new_cost + self.heuristic(self.target, next)
                    frontier.put((priority, next,))
                    came_from[next] = current

        if frontier.empty():
            print "SCANNED EVERYWHERE"
            # choose somewhere far to go
        else:
            # choose somewhere we can go
            current = self.target

        path = [current]
        while current != self.source:
            current = came_from[current]
            path.append(current)

        path.reverse()

        return path'''

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

    def cost(self, current, next, move_number):
        return 1
        if move_number > 10:
            ## hard to predict this far into the future, just ignore it
            return 1
        for projectile in self.projectile_list:
            if self.projectile_will_hit(projectile, next):
                return 999999
            
        return 1

    def projectile_will_hit(self, projectile, point):
        # returns TRUE if a projectile will hit the point
        projectile_point = Point(projectile['position'][0], projectile['position'][1])
        delta_x = projectile_point.x - point.x
        delta_y = projectile_point.y - point.y

        angle = math.atan2(delta_y, delta_x)

        distance = projectile_point.distance_to(point)
        # for safety sake, just assume the radius is always the max (2m)
        delta = math.atan2(2, distance)
        if projectile['direction'] >= angle - delta and projectile['direction'] <= angle + delta:
            #print "WILL HIT!!!"
            return True

        else:
            #print "SAFE TO GO HERE!"
            return False


class Point(object):
    def __init__(self, x, y):
        self.x = int(round(x, 0))
        self.y = int(round(y, 0))

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def distance_to(self, other):
        return math.sqrt((self.x - other.x) * (self.x - other.x) + (self.y - other.y) * (self.y - other.y))

    def toString(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"
"""
from Queue import PriorityQueue


class PathFinder(object):
    def __init__(self, mapped_area, target, source):
        self.map = mapped_area
        self.target = Point(target[0], target[1])
        self.source = Point(source[0], source[1])

    def heuristic(self, a, b):
        return abs(a.x - b.x) + abs(a.y - b.y)

    def get_path(self):
        if self.map is None or len(self.map) == 0:
            return []

        frontier = PriorityQueue()
        frontier.put((0, self.source,))
        came_from = {}
        cost_so_far = {}
        came_from[self.source] = None
        cost_so_far[self.source] = 0

        iteration_number = 0
        while not frontier.empty():
            iteration_number = iteration_number + 1
            current = frontier.get()[1]

            if abs(current.x - self.target.x) == 0 and abs(current.y - self.target.y) == 0:
                print "FOUND TARGET"
                break

            for next in self.get_neighbors(current):
                new_cost = cost_so_far[current] + self.cost(current, next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(self.target, next)
                    frontier.put((priority, next,))
                    came_from[next] = current

        if frontier.empty():
            print "SCANNED EVERYWHERE"
            # choose somewhere far to go
        else:
            # choose somewhere we can go
            current = self.target

        path = [current]
        while current != self.source:
            current = came_from[current]
            path.append(current)

        path.reverse()

        """for idx, node in enumerate(path):
            print "Node: " + str(idx) + " (" + str(node.x) + ", " + str(node.y) + ")"
        print "target: (" + str(self.target.x) + ", " + str(self.target.y) + ")"""

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
        self.x = int(round(x, 0))
        self.y = int(round(y, 0))

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def toString(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"