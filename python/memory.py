from typing import List
from timer import Timer
from apu import APU
from ppu import PPU

# https://gbdev.io/pandocs/Memory_Map.html
class Memory:
    def __init__(self, rom: str):
        self.rom: List[int] = []
        self.wram = [0] * 0x2000 # 0xC000 - 0xDFFF (8 KiB)
        self.oam = [0] * 0xA0 # 0xFE00 - 0xFE9F
        self.hram = [0] * 0x7F # 0xFF80 - 0xFFFE

        self.IF = 0x0
        self.IE = 0x0

        # components of the Gameboy that memory has access to
        self.timer = Timer()
        self.apu = APU()
        self.ppu = PPU()

        self.ticks_per_instr = 0

        # loading the "game cartridge" into our emulator
        with open(rom, "rb") as f:
            self.rom = f.read()

    def tick(self):
        self.ticks_per_instr += 1
        self.ppu.tick()
        self.apu.tick()
        self.timer.tick()

    def read(self, addr: int) -> int:
        '''
        interface for reading from memory

        :param addr: unsigned 16-bit value
        :return: byte read at address
        '''

        self.tick()

        # checking upper 4 bits to determine what region to read from quickly
        match addr >> 12:
            case 0x0 | 0x1 | 0x2 | 0x3 | 0x4 | 0x5 | 0x6 | 0x7:
                return self.rom[addr]
            case 0xC | 0xD:
                return self.wram[addr - 0xC000]
            case 0xE:
                # Nintendo says use of this area is prohibited.
                return 0xFF
            case 0xF:
                if addr <= 0xFDFF:
                    # Nintendo says use of this area is prohibited.
                    return 0xFF
                elif addr >= 0xFE00 and addr <= 0xFE9F:
                    return self.oam
                elif addr >= 0xFEA0 and addr <= 0xFEFF:
                    # Nintendo says use of this area is prohibited.
                    return 0xFF
                elif addr >= 0xFF80 and addr <= 0xFFFE:
                    return self.hram
                else:
                    # memory mapped IO + IE (interrupt enable register)
                    match addr:
                        case 0xFF44:
                            return self.ppu.LY
                        case _:
                            print("attempted to read from mmio register:", hex(addr))
                            exit(1)

        print("attempted to read to:", hex(addr))
        exit(1)

    def write(self, addr: int, value: int):
        '''
        interface for writing to memory

        :param addr: unsigned 16-bit value
        :param value: unsigned 16-bit value
        '''

        self.tick()

        match addr >> 12:
            case 0x0 | 0x1 | 0x2 | 0x3 | 0x4 | 0x5 | 0x6 | 0x7:
                self.rom[addr] = value
            case 0xC | 0xD:
                self.wram[addr - 0xC000] = value
            case 0xE:
                # Nintendo says use of this area is prohibited.
                pass
            case 0xF:
                if addr <= 0xFDFF:
                    # Nintendo says use of this area is prohibited.
                    pass
                elif addr >= 0xFE00 and addr <= 0xFE9F:
                    self.oam = value
                elif addr >= 0xFEA0 and addr <= 0xFEFF:
                    # Nintendo says use of this area is prohibited.
                    pass
                elif addr >= 0xFF80 and addr <= 0xFFFE:
                    self.hram = value
                else:
                    # memory mapped IO + IE (interrupt enable register)
                    match addr:
                        case 0xFF07:
                            self.timer.TAC = value
                        case 0xFF0F:
                            self.IF = value
                        case 0xFF26:
                            self.apu.NR52 = value
                        case 0xFF25:
                            self.apu.NR51 = value
                        case 0xFF24:
                            self.apu.NR50 = value
                        case 0xFF40:
                            self.ppu.LCDC = value
                        case 0xFFFF:
                            self.IE = value
                        case _:
                            print("attempted to write to mmio register:", hex(addr))
                            exit(1)
            case _:
                print("attempted to write to:", hex(addr))
                exit(1)






























'''
IGNORE FOR NOW:
self.vram = [0] * 0x2000 # 0x8000 - 0x9FFF (8 KiB)
self.eram = [0] * 0x2000 # 0xA000 - 0xBFFF (8 KiB)

# 0xE000 - 0xFDFF (PROHIBITED BY NINTENDO)

# 0xFEA0 - 0xFEFF (PROHIBITED BY NINTENDO)
self.mmio = [0] * 0x80


# loading the boot rom into our emulator
        with open("bootrom.bin", "rb") as f:
            self.bootrom = f.read()

REMEMBER TO ALSO SET LCDC TO 0x91
'''