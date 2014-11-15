from Queue import PriorityQueue
import math
import random


class PathFinder(object):
    def __init__(self, mapped_area, target, source, projectiles, enemies):
        self.map = mapped_area
        self.target = Point(target[0], target[1])
        self.source = Point(source[0], source[1])
        self.projectiles = projectiles
        self.enemies = enemies

    def heuristic(self, a, b):
        return abs(a.x - b.x) + abs(a.y - b.y)

    def get_path(self):
        if self.map is None or len(self.map) == 0:
            return []

        frontier = PriorityQueue()
        frontier.put((0, self.source,))
        came_from = {}
        cost_so_far = {}
        moves_so_far = {}
        came_from[self.source] = None
        cost_so_far[self.source] = 0
        moves_so_far[self.source] = 0

        interrupted = False

        while not frontier.empty():
            current = frontier.get()[1]

            if abs(current.x - self.target.x) == 0 and abs(current.y - self.target.y) == 0:
                print "FOUND TARGET"
                break

            if len(came_from) > 2000:
                interrupted = True
                print "Didn't find anything but breaking anyways"
                break

            for next in self.get_neighbors(current):
                new_cost = cost_so_far[current] + self.cost(current, next, moves_so_far[current])
                new_moves = moves_so_far[current] + 1
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    moves_so_far[next] = new_moves
                    priority = new_cost + self.heuristic(self.target, next)
                    frontier.put((priority, next,))
                    came_from[next] = current

        if frontier.empty() or interrupted:
            print "SCANNED EVERYWHERE"
            print "TARGET WASSSSSSSSS:::: ------>" + self.target.toString()
            if abs(current.x - self.target.x) != 0 or abs(current.y - self.target.y) != 0:
                # we must be on the map with all the water in the middle and there is no enemy on our side
                # go to random spots!
                current = came_from[random.choice(came_from.keys())]
        else:
            # choose somewhere we can go
            current = self.target

        path = [current]
        print "NUMBER OF POINTS VISITED: " + str(len(came_from))
        while current != self.source:
            current = came_from[current]
            path.append(current)

        path.reverse()

        """for idx, node in enumerate(path):
            print "Node: " + str(idx) + node.toString()"""

        print "Source: " + self.source.toString()
        print "Target: " + self.target.toString()
        if len(path) > 4:
            print "Nextish point: " + path[3].toString()

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

    def cost(self, current, next, moves):
        if moves > 100:  # if the algorithm is too slow, we might have to lower this value
            return 1
        else:
            cost = 1
            for projectile in self.projectiles:
                if self.projectile_will_hit(next, projectile):
                    cost = cost + 1000
            # this is too expensive
            #for enemy in self.enemies:
            #    cost = cost + self.closeness_to(enemy, next)
        return cost

    def closeness_to(self, enemy, point):
        enemy_point = Point(enemy['position'][0], enemy['position'][1])

        dist = enemy_point.distance_to(point)
        if dist == 0:
            return 1000
        else:
            return 100.0 / dist

    def projectile_will_hit(self, point, projectile):
        projectile_point = Point(projectile['position'][0], projectile['position'][1])

        length = point.x - projectile_point.x
        height = point.y - projectile_point.y

        angle = math.atan2(height, length)

        distance = point.distance_to(projectile_point)

        # always use 2 (the max radius) to be safe and keep it simple :)
        delta = math.atan2(10, distance)

        if projectile['direction'] >= angle - delta and projectile['direction'] <= angle + delta:
            return True
        else:
            return False


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

    def distance_to(self, other):
        return math.sqrt((self.x - other.x) * (self.x - other.x) + (self.y - other.y) * (self.y - other.y))
