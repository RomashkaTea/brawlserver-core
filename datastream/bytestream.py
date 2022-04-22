
class ByteStream:
    def __init__(self, buffer=b''):
        self.buffer = bytearray(buffer)
        self.offset = 0
        self.bitIdx = 0
        self.currentByte = 0
    
    def readBytes(self, length):
        array = self.buffer[self.offset:self.offset+length]
        self.offset += length
        return array
    
    def readByte(self):
        return int.from_bytes(self.readBytes(1), "big", signed=True)

    def readInt(self):
        return int.from_bytes(self.readBytes(4), "big")

    def readBoolean(self):
        if self.bitIdx == 0:
            self.currentByte = self.buffer[self.offset]
        
        result = ((1 << self.bitIdx) & self.currentByte) != 0
        self.bitIdx = (self.bitIdx + 1) & 7
        return result

    def readString(self, max=900000):
        length = self.readInt()
        if length < 0 and length > max:
            return None
        return self.readBytes(length).decode("utf-8")

    def writeBytes(self, array):
        self.bitIdx = 0
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

    def writeBoolean(self, value:bool):
        if self.bitIdx == 0:
            self.buffer += bytearray(1) # ensure
        
        if value:
            self.buffer[self.offset] |= (1 << self.bitIdx)
 
        self.bitIdx = (self.bitIdx + 1) & 7

    def writeVInt(self, value:int):
        pass # а сами сделайте.
