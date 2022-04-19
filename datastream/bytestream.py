
class ByteStream:
    def __init__(self, buffer=b''):
        self.buffer = buffer
        self.offset = 0
        self.bitIdx = 0
    
    def readBytesLength(self, length):
        array = self.buffer[self.offset:self.offset+length]
        self.offset += length
        return array
    
    def readByte(self):
        return int.from_bytes(self.readBytesLength(1), "big")

    def readInt(self):
        return int.from_bytes(self.readBytesLength(4), "big")
    
    def writeBytesLength(self, array):
        self.buffer += array
        self.offset += len(array)
    
    def writeInt(self, value:int):
        self.writeBytesLength(int.to_bytes(value, 4, "big"))
    
    def writeByte(self, value:int):
        self.writeBytesLength(int.to_bytes(value, 1, "big"))
    
    def writeVInt(self, value:int):
        pass # а сами сделайте.
