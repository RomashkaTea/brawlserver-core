from protocol.piranhamessage import PiranhaMessage
from protocol.messages.serverHello import ServerHelloMessage

class ClientHelloMessage(PiranhaMessage):
    def __init__(self):
        super().__init__()
        self.id = 10100
    
    def decode(self):
        pass # decode

    def process(self, con):
        con.messaging.send_message(ServerHelloMessage())