
class ByteStream:
    def __init__(self, buffer=b''):
        self.buffer = buffer
        self.offset = 0
        self.bitIdx = 0
    
    def readBytes(self, length):
        array = self.buffer[self.offset:self.offset+length]
        self.offset += length
        return array
    
    def readByte(self):
        return int.from_bytes(self.readBytes(1), "big")

    def readInt(self):
        return int.from_bytes(self.readBytes(4), "big")
    
    def readString(self, max=900000):
        length = self.readInt()
        if length < 0 and length > max:
            return None
        string_bytes = self.buffer[self.offset:self.offset+length]
        self.offset += length
        return string_bytes.decode("utf-8")

    def writeBytes(self, array):
        self.buffer += array
        self.offset += len(array)
    
    def writeInt(self, value:int):
        self.writeBytes(int.to_bytes(value, 4, "big"))
    
    def writeByte(self, value:int):
        self.writeBytes(int.to_bytes(value, 1, "big"))
    
    def writeString(self, value:str):
        array = value.encode("utf-8")
        self.writeInt(len(array))
        self.writeBytes(array)

    def writeVInt(self, value:int):
        pass # а сами сделайте.
