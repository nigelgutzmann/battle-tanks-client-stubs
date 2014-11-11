from command import Command
import math


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
        my_rotation = self.game_state.get_turret_rotation_for_slow()

        # the first point is the point that we are currently at, so we have to take the second one in the list
        if len(route) > 2:
            next_point = route[1]
            my_point = self.game_state.get_position_for_slow()
            print "Next Point: (" + str(next_point.x) + ", " + str(next_point.y) + ")"
            print "My Point: (" + str(my_point.x) + ", " + str(my_point.y) + ")"
            
            target_angle = self.__get_target_angle(my_point, next_point)

            print target_angle

            tank_rotate_command = commands.getTankRotateCommand(
                self.game_state.get_slow_tank_id(),
                target_angle - my_rotation
            )
            print "SENDING: " + str(tank_rotate_command)

            print self.comm.send(tank_rotate_command)

            tank_forward_command = commands.getMoveCommand(
                self.game_state.get_slow_tank_id(),
                10
            )
            print "SENDING: " + str(tank_forward_command)

            print self.comm.send(tank_forward_command)

            tank_fire_command = commansd.getFireCommand(self.game_state.get_slow_tank_id())

            print "SENDING: " + str(tank_fire_command)

            print self.comm.send(tank_fire_command)


        else:
            tank_forward_command = commands.getMoveCommand(
                self.game_state.get_slow_tank_id(),
                10,
                direction="REV"
            )

        # now look at the fast tank
        distance_to_target, position_of_target = self.game_state.get_closest_enemy_to_fast()

    def __get_target_angle(self, my_point, next_point):
        target_angle = 0
        if next_point.x > my_point.x:
            target_angle = 0
        elif next_point.x < my_point.x:
            target_angle = math.pi
        elif next_point.y < my_point.y:
            target_angle = 3 * math.pi / 2
        elif next_point.y > my_point.y:
            target_angle = math.pi / 2
        return target_angle