from protocol.piranhamessage import PiranhaMessage

class ServerHelloMessage(PiranhaMessage):
    def __init__(self):
        super().__init__()
        self.id = 20100
    
    def encode(self):
        self.stream.writeInt(24) # session key
        for i in range(24):
            self.stream.writeByte(1)