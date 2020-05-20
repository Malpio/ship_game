from app.connection_structure import tcp_socket, connection_config, response_codes, Connection
from app.game_config import default_board
import socket


class Client(Connection):
    def define_action(self, command, params):
        if command.lower() == 'your-turn':
            self.attack()
        elif command.lower() == 'hit':
            self.attack()
        elif command.lower() == 'no-hit':
            self.send_request('your-turn')
        elif command.lower() == 'already-hit':
            self.attack()
        elif command.lower() == 'attack':
            self.defense(params)
        elif command.lower() == 'incorrect-target':
            self.attack()

    def attack(self):
        target = input('Podaj współrzędne celu:')
        self.send_request('attack ' + target)

    @staticmethod
    def show_statement(code):
        try:
            print(code.upper(), ':', response_codes[code.upper()])
        except:
            print('Niezidentyfikowany kod odpowiedzi')


s = tcp_socket

try:
    s.connect(connection_config)
    client = Client(s, default_board)
    client.send_request('start')
    response = client.get_response()
    if response.lower() == 'accept':
        client.attack()
        while True:
            data = client.get_response()
            command_and_params = Connection.get_command_and_params(data)
            Client.show_statement(command_and_params['command'])
            if command_and_params['command'].lower() == 'you-won':
                client.send_request('you-lose')
                break
            elif command_and_params['command'].lower() == 'you-lose':
                client.send_request('you-won')
                break
            else:
                client.define_action(command_and_params['command'], command_and_params['params'])
    del client


except socket.error:
    print ('Error', socket.error)
