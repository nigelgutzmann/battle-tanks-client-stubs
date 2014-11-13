from command import Command
import math
from path_finding import Point


class Algorithm(object):
    def __init__(self, game_state, comm):
        self.game_state = game_state
        self.comm = comm

    def make_move(self, client_token):
        '''
        here's what really matters...
        '''

        commands = Command(client_token)

        # Let's just try to drive around first

        # work on the slow tank
        # find the closest enemy
        distance_to_target, position_of_target = self.game_state.get_closest_enemy_to_slow()

        route = self.game_state.get_route_for_slow(position_of_target)

        # route has a list of Points that we should go through to get to the target
        # now figure out the rotation
        my_rotation = self.game_state.get_track_rotation_for_slow()

        # the first point is the point that we are currently at, so we have to take the second one in the list
        next_point = None
        if len(route) > 4:
            next_point = route[3]
        elif len(route) > 3:
            next_point = route[2]
        elif len(route) > 2:
            next_point = route[1]

        if next_point:  # if we can find a next point...
            my_point = self.game_state.get_position_for_slow()
            target_angle = self.__get_target_angle(my_point, next_point)

            tank_rotate_command = commands.getTankRotateCommand(
                self.game_state.get_slow_tank_id(),
                target_angle - my_rotation
            )
            print "SENDING: ",
            print tank_rotate_command
            print self.comm.send(tank_rotate_command)

            # go forward
            tank_forward_command = commands.getMoveCommand(
                self.game_state.get_slow_tank_id(),
                10
            )
            print "SENDING ",
            print tank_forward_command
            self.comm.send(tank_forward_command)

        # get the turret rotation
        target_point = Point(position_of_target[0], position_of_target[1])
        print "TARGET POINTTTTTTTTTTT:::::::: " + target_point.toString()
        turret_angle = self.__get_target_angle(route[0], target_point)
        print "turret angle: " + str(turret_angle)
        change_turret_angle = turret_angle - self.game_state.get_slow_tank_turret_angle()
        print "current angle: " + str(self.game_state.get_slow_tank_turret_angle())
        turret_rotate_command = commands.getTurretRotateCommand(self.game_state.get_slow_tank_id(), change_turret_angle)
        print "SENDING ",
        print turret_rotate_command
        print self.comm.send(turret_rotate_command)

        # send the fire command
        tank_fire_command = commands.getFireCommand(self.game_state.get_slow_tank_id())
        self.comm.send(tank_fire_command)

        # now look at the fast tank
        distance_to_target, position_of_target = self.game_state.get_closest_enemy_to_fast()

    def __get_target_angle(self, my_point, target):

        delta_x = target.x - my_point.x
        delta_y = target.y - my_point.y

        target_angle = math.atan2(delta_y, delta_x)

        if target_angle < 0:
            target_angle = target_angle + 2 * math.pi
        if target_angle > 2 * math.pi:
            target_angle = target_angle - 2 * math.pi
        return target_angle
