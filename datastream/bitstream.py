# this bitstream by xeondev1337

class BitStream:
    def __init__(self, buff=b''):
        self.buffer = buff
        self.bitIndex = 0
        self.offset = 0
    
    def readBit(self):
        if self.offset > len(self.buffer):
            print("Out of range!")
            return 0
        value = (self.buffer[self.offset] >> self.bitIndex) & 1
        self.bitIndex += 1
        if (self.bitIndex == 8):
            self.bitIndex = 0
            self.offset += 1
        return value
    
    def readBytes(self, length):
        data = []
        i = 0
        while i < length:
            value = 0
            p = 0
            while p < 8 and i < length:
                value |= self.readBit() << p
                i += 1
                p += 1
            data.append(value)
        return bytes(data)
    
    def readPositiveInt(self, bitsCount):
        data = self.readBytes(bitsCount)
        return int.from_bytes(data, "little")
    
    def readInt(self, bitsCount):
        v2 = 2 * self.readPositiveInt(1) - 1
        return v2 * self.readPositiveInt(bitsCount)
    
    def readPositiveVIntMax255(self):
        v2 = self.readPositiveInt(3)
        return self.readPositiveInt(v2)
    
    def readPositiveVIntMax65535(self):
        v2 = self.readPositiveInt(4)
        return self.readPositiveInt(v2)
    
    def readPositiveVIntMax255OftenZero(self):
        if self.readBoolean(): return 0
        return self.readPositiveVIntMax255()
        
    def readPositiveVIntMax65535OftenZero(self):
        if self.readBoolean(): return 0
        return self.readPositiveVIntMax65535()
        
    def readBoolean(self):
        return self.readPositiveInt(1) == 1
    
    def writeBit(self, data):
        if (self.bitIndex == 0):
            self.offset += 1
            self.buffer += b'\xff'
        
        value = self.buffer[self.offset - 1]
        value &= ~(1 << self.bitIndex)
        value |= (data << self.bitIndex)
        self.buffer[self.offset - 1] = value
        
        self.bitIndex = (self.bitIndex + 1) % 8
    
    def writeBits(self, bits, count):
        i = 0
        position = 0
        while i < count:
            value = 0
            
            p = 0
            while p < 8 and i < count:
                value = (bits[position] >> p) & 1
                self.writeBit(value)
                p += 1
                i += 1
            position += 1
    
    def writePositiveInt(self, value, bitsCount):
        self.writeBits(value.to_bytes(4, byteorder='little'), bitsCount)

    def writeInt(self, value, bitsCount):
        val = value
        if val <= -1:
            self.writePositiveInt(0, 1)
            val = -value
        elif val >= 0:
            self.writePositiveInt(1, 1)
            val = value
        self.writePositiveInt(val, bitsCount)
    
    def writePositiveVInt(self, value, count):
        v3 = 1
        v7 = value
        
        if v7 != 0:
            if (v7 < 1):
                v3 = 0
            else:
                v8 = v7
                v3 = 0
                
                v3 += 1
                v8 >>= 1
                
                while (v8 != 0):
                    v3 += 1
                    v8 >>= 1
        self.writePositiveInt(v3 - 1, count)
        self.writePositiveInt(v7, v3)
    
    def writePositiveVIntMax255(self, value:int):
        self.writePositiveVInt(value, 3)
    
    def writePositiveVIntMax65535(self, value:int):
        self.writePositiveVInt(value, 4)
    
    def writePositiveVIntMax255OftenZero(self, value:int):
        if value == 0:
            self.writePositiveInt(1, 1)
            return
        self.writePositiveInt(0, 1)
        self.writePositiveVInt(value, 3)
        
    def writePositiveVIntMax65535OftenZero(self, value:int):
        if value == 0:
            self.writePositiveInt(1, 1)
            return
        self.writePositiveInt(0, 1)
        self.writePositiveVInt(value, 4)
        
    def writeBoolean(self, value:bool):
        if value: self.writePositiveInt(1, 1)
        else: self.writePositiveInt(0, 1)
    
