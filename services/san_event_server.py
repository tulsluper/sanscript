#!/usr/bin/env python3

import logging
import json
import socket

from san_event_handler import handle

try:
    from settings import EVENT_HOST as HOST
    from settings import EVENT_PORT as PORT
except:
    HOST = '0.0.0.0'
    PORT = 50501


def listen():

    logger = logging.getLogger(__name__)

    serversocket = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((HOST, PORT))
    serversocket.listen(1)

    while True:
        connection, address = serversocket.accept()
        message = connection.recv(256).decode()
        message = json.loads(message)
        handle(message)
    

if __name__ == '__main__':
    listen()
