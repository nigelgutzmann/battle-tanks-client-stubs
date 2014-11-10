import command
import communication


class Player(object):
    def __init__(self, comm, game_info):
        self.commands = command.Command()
        self.comm = comm
        self.game_info = game_info

    def play_game(self):
        while True:
            # get a message
            message = self.comm.receive(communication.Communication.Origin.PublishSocket)

            # decode it
            print message

            # decide what to do

            # send something
