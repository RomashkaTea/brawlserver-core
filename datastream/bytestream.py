
class ByteStream:
    def __init__(self, buffer=b''):
        self.buffer = bytearray(buffer)
        self.offset = 0
        self.bit_idx = 0
    
    def read_bytes(self, length):
        array = self.buffer[self.offset:self.offset+length]
        self.offset += length
        return array
    
    def read_byte(self):
        self.bit_idx = 0
        return int.from_bytes(self.read_bytes(1), "big", signed=True)

    def read_int16(self):
        self.bit_idx = 0
        return int.from_bytes(self.read_bytes(2), "big")

    def read_int24(self):
        self.bit_idx = 0
        return int.from_bytes(self.read_bytes(3), "big")

    def read_int(self):
        self.bit_idx = 0
        return int.from_bytes(self.read_bytes(4), "big")

    def read_boolean(self):
        if self.bit_idx == 0:
            self.offset += 1

        result = (self.buffer[self.offset - 1] & (1 << self.bit_idx)) != 0
        self.bit_idx = (self.bit_idx + 1) & 7
        return result

    def read_string(self, max=900000):
        length = self.read_int()
        if length < 0 and length > max:
            return None
        return self.read_bytes(length).decode("utf-8")

    def write_bytes(self, array):
        self.bit_idx = 0
        self.buffer += array
        self.offset += len(array)
    
    def write_int16(self, value:int):
        self.write_bytes(int.to_bytes(value, 2, "big"))

    def write_int24(self, value:int):
        self.write_bytes(int.to_bytes(value, 3, "big"))

    def write_int(self, value:int):
        self.write_bytes(int.to_bytes(value, 4, "big"))
    
    def write_byte(self, value:int):
        self.write_bytes(int.to_bytes(value, 1, "big"))
    
    def write_string(self, value:str):
        array = value.encode("utf-8")
        self.write_int(len(array))
        self.write_bytes(array)

    def write_boolean(self, value:bool):
        if self.bit_idx == 0:
            self.buffer += bytearray(1) # ensure
            self.offset += 1
        
        if value:
            self.buffer[self.offset - 1] |= (1 << self.bit_idx)
 
        self.bit_idx = (self.bit_idx + 1) & 7

    # there must be a better way to do this
    def convert_unsigned_to_signed(unsigned:int):
        return int.from_bytes(int.to_bytes(unsigned, 4, "big"), "big", signed=True)

    def read_vint(self):
        byte = self.read_byte()

        if (byte & 0x40) != 0:
            result = byte & 0x3f
            if (byte & 0x80) != 0:
                byte = self.read_byte()
                result |= (byte & 0x7f) << 6
                if (byte & 0x80) != 0:
                    byte = self.read_byte() 
                    result |= (byte & 0x7f) << 13
                    if (byte & 0x80) != 0:
                        byte = self.read_byte()
                        result |= (byte & 0x7f) << 20
                        if (byte & 0x80) != 0:
                            byte = self.read_byte()
                            result |= (byte & 0x7f) << 27
                            return ByteStream.convert_unsigned_to_signed(result | 0x80000000)
                        return ByteStream.convert_unsigned_to_signed(result | 0xF8000000)
                    return ByteStream.convert_unsigned_to_signed(result | 0xFFF00000)
                return ByteStream.convert_unsigned_to_signed(result | 0xFFFFE000)
            return ByteStream.convert_unsigned_to_signed(result | 0xFFFFFFC0)
        else:
            result = byte & 0x3f

            if (byte & 0x80) != 0:
                byte = self.read_byte()
                result |= (byte & 0x7f) << 6
                if (byte & 0x80) != 0:
                    byte = self.read_byte()
                    result |= (byte & 0x7f) << 13
                    if (byte & 0x80) != 0:
                        byte = self.read_byte()
                        result |= (byte & 0x7f) << 20
                        if (byte & 0x80) != 0:
                            byte = self.read_byte()
                            result |= (byte & 0x7f) << 27
            return result
    
    def write_vint(self, value:int):
        tmp = (value >> 25) & 0x40
        flipped = value ^ (value >> 31)

        tmp |= value & 0x3F
        value >>= 6
        flipped >>= 6

        if flipped == 0:
            self.write_byte(tmp)
            return
        
        self.write_byte(tmp | 0x80)
        flipped >>= 7
        r = 0
        if flipped != 0:
            r = 0x80
           
        self.write_byte((value & 0x7F) | r)
        value >>= 7

        while flipped != 0:
            flipped >>= 7
            r = 0
            if flipped != 0:
                    r = 0x80
            self.write_byte((value & 0x7F) | r)
            value >>= 7

    def set_offset(self, offset: int):
        self.offset = offset
        self.bit_idx = 0