from cpu import CPU

cpu = CPU("test_roms/cpu_instrs.gb")

while True:
    cpu.render_frame()
