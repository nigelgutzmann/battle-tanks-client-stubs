import json


class PublishDecoder(object):
    def __init__(self, game_info):
        self.game_info = game_info

    def decode(self, message, game_state):
        try:
            message_data = json.loads(message)
        except:
            # sometimes it just returns the game token, which isn't json.
            # just drop it
            print "non-json received!"
            return None

        if message_data['comm_type'] == 'GAME_START':
            print "GAME_START received!"
            # who cares.
            return None

        elif message_data['comm_type'] == 'GAME_END':
            print "GAME_END received!"
            game_state.reset()

        elif message_data['comm_type'] == "MATCH_END":
            print "MATCH_END received!"
            game_state.reset()

        elif message_data['comm_type'] == "GAMESTATE":
            # we have a gamestate packet
            print "GAMESTATE received!"
            if game_state.boundaries_unset():
                # set up the map, should only have to do this stuff once
                game_state.set_boundaries(x=message_data['map']['size'][0], y=message_data['map']['size'][1])
                game_state.set_terrain(terrain=message_data['map']['terrain'])
                game_state.print_map()

            # get the players
            players = message_data['players']
            our_team = {}
            other_team = {}
            for player in players:
                if player['name'] == game_info.team_name:
                    # this is us!
                    our_team = player
                else:
                    other_team = player

            # find the fast and slow tank
            our_slow = self.__get_slow(our_team)
            our_fast = self.__get_fast(our_team)
            enemy_slow = self.__get_slow(other_team)
            enemy_fast = self.__get_fast(other_team)

            # save the data
            game_state.set_enemy_position(slow_tank=enemy_slow, fast_tank=enemy_fast)
            game_state.set_my_position(slow_tank=our_slow, fast_tank=our_fast)

    def __get_slow(player):
        for tank in player['tanks']:
            if tank['type'] == 'TankSlow':
                return tank
        return None

    def __get_fast(player):
        for tank in player['tanks']:
            if tank['type'] == 'TankFast':
                return tank
        return None
