
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
        self.bitIdx = 0
        return int.from_bytes(self.readBytes(1), "big", signed=True)

    def readInt(self):
        self.bitIdx = 0
        return int.from_bytes(self.readBytes(4), "big")

    def readBoolean(self):
        if self.bitIdx == 0:
            self.currentByte = int.from_bytes(self.readBytes(1), "big", signed=True)
        
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

    def convert_unsigned_to_signed(unsigned:int): # python is dudnik lang :upside_down: 
        return int.from_bytes(int.to_bytes(unsigned, 4, "big"), "big", signed=True)

    def readVInt(self):
        byte = self.readByte()

        if (byte & 0x40) != 0:
            result = byte & 0x3f
            if (byte & 0x80) != 0:
                byte = self.readByte()
                result |= (byte & 0x7f) << 6
                if (byte & 0x80) != 0:
                    byte = self.readByte() 
                    result |= (byte & 0x7f) << 13
                    if (byte & 0x80) != 0:
                        byte = self.readByte()
                        result |= (byte & 0x7f) << 20
                        if (byte & 0x80) != 0:
                            byte = self.readByte()
                            result |= (byte & 0x7f) << 27
                            return ByteStream.convert_unsigned_to_signed(result | 0x80000000)
                        return ByteStream.convert_unsigned_to_signed(result | 0xF8000000)
                    return ByteStream.convert_unsigned_to_signed(result | 0xFFF00000)
                return ByteStream.convert_unsigned_to_signed(result | 0xFFFFE000)
            return ByteStream.convert_unsigned_to_signed(result | 0xFFFFFFC0)
        else:
            result = byte & 0x3f

            if (byte & 0x80) != 0:
                byte = self.readByte()
                result |= (byte & 0x7f) << 6
                if (byte & 0x80) != 0:
                    byte = self.readByte()
                    result |= (byte & 0x7f) << 13
                    if (byte & 0x80) != 0:
                        byte = self.readByte()
                        result |= (byte & 0x7f) << 20
                        if (byte & 0x80) != 0:
                            byte = self.readByte()
                            result |= (byte & 0x7f) << 27
            return result
    
    def writeVInt(self, value:int):
        tmp = (value >> 25) & 0x40
        flipped = value ^ (value >> 31)

        tmp |= value & 0x3F
        value >>= 6
        flipped >>= 6

        if flipped == 0:
            self.writeByte(tmp)
            return
        
        self.writeByte(tmp | 0x80)
        flipped >>= 7
        r = 0
        if flipped != 0:
            r = 0x80
           
        self.writeByte((value & 0x7F) | r)
        value >>= 7

        while flipped != 0:
            flipped >>= 7
            r = 0
            if flipped != 0:
                    r = 0x80
            self.writeByte((value & 0x7F) | r)
            value >>= 7
