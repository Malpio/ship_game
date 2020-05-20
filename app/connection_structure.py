import socket

tcp_socket = serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
connection_config = ('127.0.0.1', 40000)

response_codes = {
    'ACCEPT': 'Zaakceptowano prośbę o rozpoczęcie rozgrywki',
    'DISCARD': 'Odrzucono prośbę o rozpoczęcie rozgrywki',
    'ATTACK': 'Zaatakowano Cię',
    'YOUR-TURN': 'Twoja kolej',
    'HIT': 'Trafiłeś w cel!',
    'NO-HIT': 'Nie trafiłeś',
    'ALREADY-HIT': 'Już strzelałeś pod te współrzędne',
    'INCORRECT-TARGET': 'Podałeś nieprawidłowy cel. Spróbuj raz jeszcze',
    'YOU-WON': 'Wygrałeś',
    'YOU-LOSE': 'Przegrałeś',
}


class Connection:
    def __init__(self, connection, board):
        self.connection = connection
        self.board = board
        self.countOfShotTarget = 0
        print(self.board)

    def __del__(self):
        self.connection.close()
        print('Połączenie zakończone')

    def send_request(self, request):
        request = request + '\r\n'
        self.connection.sendall(request.encode())

    def get_response(self):
        response = b''
        while not b'\r\n' in response:
            data = self.connection.recv(1)
            response += data
        response = response.decode()[:-2]
        return response

    @staticmethod
    def get_command_and_params(response):
        try:
            array = response.split(' ')
            command = array[0]
            params = array[1:]
            return {'command': command, 'params': params}
        except:
            array = response.split(' ')
            command = array[0]
            return {'command': command, 'params': []}

    def defense(self, target):
        print('Zaatakowana pozycja: ', target[0].upper())
        try:
            if self.board[target[0].upper()].lower() == '[o]':
                print('Trafił Cię!')
                self.countOfShotTarget += 1
                self.board[target[0].upper()] = '[x]'
                if self.countOfShotTarget == 17:
                    self.send_request('you-won')
                else:
                    self.send_request('hit')

            elif self.board[target[0].upper()].lower() == '[x]':
                print('Zaatakował wcześniej trafioną pozycję!')
                self.send_request('already-hit')
            else:
                print('Nie trafił Cię!')
                self.send_request('no-hit')
        except:
            self.send_request('incorrect-target')
