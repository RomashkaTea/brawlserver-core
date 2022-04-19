from ast import Bytes
#from network.connection import Connection
from datastream.bytestream import ByteStream

class PiranhaMessage:
    def __init__(self):
        self.id = 0
        self.version = 0
        self.stream = ByteStream()
    
    def encode(self): pass
    def decode(self): pass
    def process(self, con): pass