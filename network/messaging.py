from protocol.piranhamessage import PiranhaMessage

class Messaging:
    def __init__(self, con):
        self.connection = con
    
    async def send_message(self, message : PiranhaMessage):
        if len(message.stream.buffer) == 0:
            message.encode()
        
        header = Messaging.write_header(message.id, len(message.stream.buffer), message.version)

        await self.connection.send(header + message.stream.buffer)

        print(f"sent message with id {message.id}, length: {len(message.stream.buffer)}")

    @staticmethod
    def write_header(type, length, version):
        buffer = b''
        buffer += int.to_bytes(type, 2, "big")
        buffer += int.to_bytes(length, 3, "big")
        buffer += int.to_bytes(version, 2, "big")
        return buffer

    @staticmethod
    def read_header(buffer):
        return int.from_bytes(buffer[:2], "big"), int.from_bytes(buffer[2:5], "big"), int.from_bytes(buffer[5:], "big")