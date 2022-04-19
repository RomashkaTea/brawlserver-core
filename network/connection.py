import socket

from network.messaging import Messaging
from protocol.messageFactory import MessageFactory

class Connection:
    def __init__(self, sock):
        self.socket = sock
        self.messaging = Messaging(self)

    def send(self, buffer):
        self.socket.send(buffer)
    
    def receive_message(self):
        try:
            header = self.socket.recv(7)
            if len(header) > 0:
                message_type, length, version = Messaging.readHeader(header)
                payload = self.socket.recv(length)
                print(f"received message {message_type}, length {length}, version {version}")
                message = MessageFactory.create_message_by_type(message_type)
                if message != None:
                    message.stream.buffer = payload
                    message.decode()
                    message.process(self)
                return 0
        except:
            return -1