from protocol.piranhamessage import PiranhaMessage

class Messaging:
    def __init__(self, con):
        self.connection = con
    
    def send_message(self, message : PiranhaMessage):
        if len(message.stream.buffer) == 0:
            message.encode()
        header = Messaging.writeHeader(message.id, len(message.stream.buffer), message.version)
        self.connection.send(header + message.stream.buffer)
        print(f"sent message with id {message.id}, length: {len(message.stream.buffer)}")

    @staticmethod
    def writeHeader(type, length, version):
        buffer = b''
        buffer += int.to_bytes(type, 2, "big")
        buffer += int.to_bytes(length, 3, "big")
        buffer += int.to_bytes(version, 2, "big")
        return buffer

    @staticmethod
    def readHeader(buffer):
        return int.from_bytes(buffer[:2], "big"), int.from_bytes(buffer[2:5], "big"), int.from_bytes(buffer[5:], "big")