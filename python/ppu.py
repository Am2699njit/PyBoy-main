class PPU:
    def __init__(self):
        self.LY = 0
        self.LCDC = 0x0
        self.frame = [[0] * 160] * 144

    def tick(self):
        pass