from protocol.piranhamessage import PiranhaMessage

class ServerHelloMessage(PiranhaMessage):
    def __init__(self):
        super().__init__()
        self.id = 20100
    
    def encode(self):
        self.stream.write_int(24) # session key
        for i in range(24): # this is not recommended for production, the session key should be random
            self.stream.write_byte(1)