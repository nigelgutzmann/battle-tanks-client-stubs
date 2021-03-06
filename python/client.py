import sys
import optparse
import gameinfo
import command
import communication
import player


class Client(object):
    """
    The main client class. Responsible for running the game.
    """
    def __init__(self, match_token=None, host_name=None):

        """
        Constructor
        """

        parser = optparse.OptionParser()
        parser.add_option('-t', help='specifies the team name', dest='team_name')
        parser.add_option('-p', help='specifies the teams password', dest='team_password')
        parser.add_option('-m', help='specifies the match token', dest='match_token')
        parser.add_option('-n', help='specifies the host name (optional)', dest='host_name')

        global opts
        (opts, args) = parser.parse_args()

        if opts.team_name is None or 0 == len(opts.team_name):
            opts.team_name = 'ThinkTank2.0'

        if opts.match_token is None or 0 == len(opts.match_token):
            if match_token:
                opts.match_token = match_token
            else:
                print "match token is mandatory"
                parser.print_help()
                exit(1)

        if opts.team_password is None or 0 == len(opts.team_password):
            opts.team_password = 'th1nk'

        if opts.host_name is None or 0 == len(opts.host_name):
            if host_name:
                opts.host_name = host_name
            else:
                print "host name is mandatory"
                parser.print_help()
                exit(1)

        self.game_info = gameinfo.GameInfo(opts.team_name, opts.match_token, opts.team_password)
        self.cmd = command.Command()
        self.comm = communication.Communication(opts.host_name)
        self.player = None

    def run(self):
        """
        Runs the game
        """
        print "Starting Battle Tanks Client..."

        connect_command = self.cmd.getMatchConnectCommand(
            self.game_info.team_name, self.game_info.match_token, self.game_info.team_password
        )

        print 'Connecting to server...'
        self.comm.set_subscription(opts.match_token)
        self.game_info.client_token = self.comm.send(connect_command, self.cmd.CLIENT_TOKEN)

        print 'Received client token... %s' % self.game_info.client_token
        print 'Starting game...'

        self.player =  player.Player(self.comm, self.game_info, self.game_info.client_token)
        self.player.play_game()

        print 'Exiting...'
        exit()

    def exit(self):
        """
        cleanup and exit
        """
        self.comm.close()

if __name__ == "__main__":
    client = Client()
    try:
        client.run()
    except (SystemExit, KeyboardInterrupt):
        client.exit()
