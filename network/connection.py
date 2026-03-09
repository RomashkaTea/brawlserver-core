import socket

from network.messaging import Messaging
from protocol.messageFactory import MessageFactory

class Connection:
    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer
        self.messaging = Messaging(self)

    async def send(self, buffer):
        self.writer.write(buffer)
        await self.writer.drain()
    
    async def receive_message(self):
        header = await self.reader.readexactly(7)

        message_type, length, version = Messaging.read_header(header)
        if length > 10000: # a normal client message can't be longer
            return -1 
        
        payload = await self.reader.readexactly(length)

        print(f"received message {message_type}, length {length}, version {version}")
                
        message = MessageFactory.create_message_by_type(message_type)
        if message != None:
            message.stream.buffer = payload
            message.decode()
            await message.process(self)

        return 0