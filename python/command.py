import json
import gameinfo


class Command(object):
    """
    creates json commands that can be sent to the server
    """
    CLIENT_TOKEN = 'client_token'
    COMM_TYPE = 'comm_type'
    NUM_PLAYERS = 'num_players'
    TEAM_NAME = 'team_name'
    MATCH_TOKEN = 'match_token'
    PASSWORD = 'password'
    GAME_MOVE = 'GameMove'
    GAME_END = 'GameEnd'
    MATCH_END = 'MatchEnd'

    def __init__(self, client_token=None):
        self.client_token = client_token

    def getMatchConnectCommand(self, team_name, match_token, team_password):
        """
        returns a json command to connect to an established match.
        """
        dict = {}
        dict[Command.COMM_TYPE] = CommType.MATCH_CONNECT
        dict[Command.TEAM_NAME] = team_name
        dict[Command.MATCH_TOKEN] = match_token
        dict[Command.PASSWORD] = team_password
        return json.dumps(dict)

    def getMoveCommand(self, tank_id, distance, direction="FWD"):
        return json.dumps({
            "tank_id": tank_id,
            "comm_type": "MOVE",
            "direction": direction,
            "distance": distance,
            "client_token": self.client_token,
        })

    def getTankRotateCommand(self, tank_id, rads):
        direction = "CCW"
        if rads < 0:
            rads = rads * -1
            direction = "CW"
        return json.dumps({
            "tank_id": tank_id,
            "comm_type": "ROTATE",
            "direction": direction,
            "rads": rads,
            "client_token": self.client_token,
        })

    def getTurretRotateCommand(self, tank_id, rads, direction="CW"):
        return json.dumps({
            "tank_id": tank_id,
            "comm_type": "ROTATE_TURRET",
            "direction": direction,
            "rads": rads,
            "client_token": self.client_token,
        })

    def getFireCommand(self, tank_id):
        return json.dumps({
            "tank_id": tank_id,
            "comm_type": "FIRE",
            "client_token": self.client_token,
        })

    def getStopCommand(self, tank_id, control):
        return json.dumps({
            "tank_id": tank_id,
            "comm_type": "STOP",
            "control": control,
            'client_token': self.client_token,
        })


class CommType(object):
    MATCH_CONNECT = 'MatchConnect'
