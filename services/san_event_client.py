#!/usr/bin/env python3

import socket
import json

try:
    from settings import EVENT_HOST as HOST
    from settings import EVENT_PORT as PORT
except:
    HOST = '0.0.0.0'
    PORT = 50501


def send_event(event, data):
    clientsocket = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((HOST, PORT))
    message = json.dumps({
        'event': event,
        'data': data,
    }).encode()
    print('data', data)
    clientsocket.send(message)
    return


if __name__ == '__main__':
    send_event('test', {'message': 'SANscript'})
