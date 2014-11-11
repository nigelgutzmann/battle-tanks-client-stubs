import command
import communication
from publish_decoder import PublishDecoder
from game_state import GameState
from algorithm import Algorithm


class Player(object):
    def __init__(self, comm, game_info):
        self.commands = command.Command()
        self.comm = comm
        self.game_info = game_info
        self.pub_decoder = PublishDecoder(game_info)
        self.game_state = GameState()
        self.algorithm = Algorithm(self.game_state, self.comm)

    def play_game(self, client_token):
        # TODO: later, we will want to spawn two threads here
        while True:
            # get a message
            message = self.comm.receive(communication.Communication.Origin.PublishSocket)

            # decode it
            self.pub_decoder.decode(message, self.game_state)

            # decide what to do
            self.algorithm.make_move(client_token)
