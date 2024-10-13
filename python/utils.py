def i8(v: int) -> int:
    return ((v & 0xFF) ^ 0x80) - 0x80

def u16(v: int) -> int:
    return v & 0xFFFF