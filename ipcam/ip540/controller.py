import base64
from http.client import HTTPConnection, responses

class Controller:

    _MOVE = '/cgi-bin/view/cammove.cgi?move={direction}'
    _SPEED = '/cgi-bin/view/ptzspeed.cgi?speed={speed}'

    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'
    UP_LEFT = 'upleft'
    UP_RIGHT = 'upright'
    DOWN_LEFT = 'downleft'
    DOWN_RIGHT = 'downright'
    HOME = 'home'

    _AUTHORIZATION_HEADER = 'Basic {0}'
    _AUTHORIZATION_HEADER_BASE64_USERNAME_PASSWORD = '{username}:{password}'

    def __init__(self, control_address, admin_username, admin_password):
        self.connection = HTTPConnection(control_address)
        self.address = control_address
        self.username = admin_username
        self.password = admin_password

    def __get_request(self, url):
        authorization_header = Controller._AUTHORIZATION_HEADER.format(base64.encodebytes(
            Controller._AUTHORIZATION_HEADER_BASE64_USERNAME_PASSWORD.format(**{
                'username': self.username,
                'password': self.password,
            }).encode()
        )[:-1].decode())

        self.connection.request(
            method='GET',
            url=url,
            headers={
                'Host': self.address,
                'Connection': 'close',
                'Authorization': authorization_header,
            }
        )

        return self.connection.getresponse().status == 200

    def move(self, direction):
        return self.__get_request(Controller._MOVE.format(direction=direction))

    def set_speed(self, speed):
        return self.__get_request(Controller._SPEED.format(speed=speed))
