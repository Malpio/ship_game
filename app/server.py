from app.connection_structure import tcp_socket, connection_config, Connection
from app.game_config import default_board, targets
import random

server_socket = tcp_socket
server_socket.bind(connection_config)
server_socket.listen(5)


class Server(Connection):
    def define_action(self, command, params):
        if command.lower() == 'your-turn':
            self.attack()
        elif command.lower() == 'start':
            self.send_request('accept')
        elif command.lower() == 'hit':
            self.attack()
        elif command.lower() == 'already-hit':
            self.attack()
        elif command.lower() == 'no-hit':
            self.send_request('your-turn')
        elif command.lower() == 'attack':
            self.defense(params)
        elif command.lower() == 'incorrect-target':
            self.attack()

    def attack(self):
        index = random.randint(0, 100)
        target = targets[index]
        self.send_request('attack ' + target)


while True:
    client, addr = server_socket.accept()
    board = default_board
    client_connection = Server(client, board)
    while True:
        data = client_connection.get_response()
        command_and_params = Connection.get_command_and_params(data)
        if command_and_params['command'].lower() == 'you-won':
            client_connection.send_request('you-lose')
            break
        elif command_and_params['command'].lower() == 'you-lose':
            client_connection.send_request('you-won')
            break
        else:
            client_connection.define_action(command_and_params['command'], command_and_params['params'])
    del client_connection
