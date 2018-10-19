import urllib.request
import base64
import cv2
import numpy as np
import sys


def main():
    try:
        host = sys.argv[1]
        port = str(sys.argv[2])
        username = sys.argv[3]
        password = ''
    except:
        print('Usage: python3 ', sys.argv[0], ' <hostname> <port> <username> [password]')
        exit(1)
    try:
        password = sys.argv[4]
    except:
        pass

    print('Host: ', host)
    print('Port: ', port)
    print('Username: ', username)
    print('Password: ', password)

    auth = username + ':' + password
    auth = base64.b64encode(auth.encode('ascii')).decode('ascii')

    request = urllib.request.Request('http://' + host + ':' + port + '/videostream.cgi', headers={'Authorization': 'Basic ' + auth})
    stream = urllib.request.urlopen(request)
    buffer = bytes()
    # print(type(stream))
    # print(stream.status)
    # print(stream.getheaders())

    start = b'\xff\xd8'
    end = b'\xff\xd9'

    if stream.status == 200:
        while not stream.closed:
            buffer += stream.read(2048)
            a = buffer.find(start)
            b = buffer.find(end)
            if a != -1 and b != -1:
                # print('aa')
                img = buffer[a:b]
                img = np.fromstring(img, np.uint8)
                img = cv2.imdecode(img, 1)
                cv2.imshow('img', img)
                buffer = buffer[b+2:]
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break


if __name__ == '__main__':
    main()
