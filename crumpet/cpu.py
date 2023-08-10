import math
import random as rd


class CPU:
    def __init__(self, master):
        self.renderer = master.renderer
        self.keyboard = master.keyboard

        # 4 KB of memory
        self.memory = [None]*4096
        # 16 8bit registers
        self.v = [0]*16
        # register
        self.i = 0

        self.delaytimer = 0

        # program counter
        self.pc = 0x200
        
        self.stack = []
        self.paused = False
        self.speed = 10

    def load_sprites(self):
        sprites = [
            0xF0, 0x90, 0x90, 0x90, 0xF0, # 0
            0x20, 0x60, 0x20, 0x20, 0x70, # 1
            0xF0, 0x10, 0xF0, 0x80, 0xF0, # 2
            0xF0, 0x10, 0xF0, 0x10, 0xF0, # 3
            0x90, 0x90, 0xF0, 0x10, 0x10, # 4
            0xF0, 0x80, 0xF0, 0x10, 0xF0, # 5
            0xF0, 0x80, 0xF0, 0x90, 0xF0, # 6
            0xF0, 0x10, 0x20, 0x40, 0x40, # 7
            0xF0, 0x90, 0xF0, 0x90, 0xF0, # 8
            0xF0, 0x90, 0xF0, 0x10, 0xF0, # 9
            0xF0, 0x90, 0xF0, 0x90, 0x90, # A
            0xE0, 0x90, 0xE0, 0x90, 0xE0, # B
            0xF0, 0x80, 0x80, 0x80, 0xF0, # C
            0xE0, 0x90, 0x90, 0x90, 0xE0, # D
            0xF0, 0x80, 0xF0, 0x80, 0xF0, # E
            0xF0, 0x80, 0xF0, 0x80, 0x80  # F
        ]

        for i, sprite in enumerate(sprites):
            self.memory[i] = sprite

    def load_program(self, program):
        for loc, opcode in enumerate(program):
            self.memory[self.pc + loc] = opcode
            
    def load_rom(self, rom):
        with open(rom, 'rb') as fp:
            self.load_program(list(fp.read()))
    
    def cycle(self):
        for i in range(self.speed):
            if not self.paused:
                opcode = (self.memory[self.pc] << 8 | self.memory[self.pc + 1])
                try:
                    self.execute_instruction(opcode)
                except:
                    pass
                
        if not self.paused:
            self.update_timers()

        self.renderer.render()

    def update_timers(self):
        if self.delaytimer > 0:
            self.delaytimer -= 1

    def execute_instruction(self, opcode):
        # each instruction is 2 bytes
        self.pc += 2

        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4

        match (opcode & 0xF000):
            case 0x0000:
                match opcode:
                    case 0x00E0:
                        self.renderer.clear()
                    case 0x00EE:
                        self.pc = self.stack.pop()
                    case _: ...
            case 0x1000:
                self.pc = (opcode & 0xFFF)
            case 0x2000:
                self.stack.append(self.pc)
                self.pc = (opcode & 0xFFF)
            case 0x3000:
                if self.v[x] == (opcode & 0xFF):
                    self.pc += 2
            case 0x4000:
                if self.v[x] != (opcode & 0xFF):
                    self.pc += 2
            case 0x5000:
                if self.v[x] == self.v[y]:
                    self.pc += 2
            case 0x6000:
                self.v[x] = (opcode & 0xFF)
            case 0x7000:
                self.v[x] += (opcode & 0xFF)
            case 0x8000:
                match (opcode & 0xF):
                    case 0x0:
                        self.v[x] = self.v[y]
                    case 0x1:
                        self.v[x] |= self.v[y]
                    case 0x2:
                        self.v[x] &= self.v[y]
                    case 0x3:
                        self.v[x] ^= self.v[y]
                    case 0x4:
                        self.v[x] += self.v[y]
                        sum = self.v[x]

                        self.v[0xF] = 0

                        if sum > 0xFF:
                            self.v[0xF] = 1

                        self.v[x] = sum
                    case 0x5:
                        self.v[0xF] = 0

                        if self.v[x] > self.v[y]:
                            self.v[0xF] = 1

                        self.v[x] -= self.v[y]
                    case 0x6:
                        self.v[0xF] = (self.v[x] & 0x1)
                        self.v[x] >>= 1
                    case 0x7:
                        self.v[0xF] = 0

                        if self.v[y] > self.v[x]:
                            self.v[0xF] = 1

                        self.v[x] = self.v[y] - self.v[x]
                    case 0xE:
                        self.v[0xF] = (self.v[x] & 0x80)
                        self.v[x] <<= 1
                    case _: ...
            case 0x9000:
                if self.v[x] != self.v[y]:
                    self.pc += 2
            case 0xA000:
                self.i = (opcode & 0xFFF)
            case 0xB000:
                self.pc = (opcode & 0xFFF) + self.v[0]
            case 0xC000:
                rand = math.floor(rd.randint(0, 255) * 0xFF)
                self.v[x] = rand & (opcode & 0xFF)
            case 0xD000:
                width = 8
                height = (opcode & 0xF)

                self.v[0xF] = 0

                for row in range(height):
                    sprite = self.memory[self.i + row]
                    if sprite is None:
                        continue
                    for col in range(width):
                        if (sprite & 0x80) > 0:
                            try:
                                if self.renderer.set_pixel(self.v[x] + col, self.v[y] + row):
                                    self.v[0xF] = 1
                            except IndexError:
                                pass
                        sprite <<= 1
                
            case 0xE000:
                match (opcode & 0xFF):
                    case 0x9E:
                        if self.keyboard.is_key_pressed(self.v[x]):
                            self.pc += 2
                    case 0xA1:
                        if not self.keyboard.is_key_pressed(self.v[x]):
                            self.pc += 2
                    case _: ...
            case 0xF000:
                match (opcode & 0xFF):
                    case 0x07:
                        self.v[x] = self.delaytimer
                    case 0x0A:
                        self.paused = True

                        def temp(key):
                            self.v[x] = key
                            self.paused = False

                        self.keyboard.on_next = temp 
                    case 0x15:
                        self.delaytimer = self.v[x]
                    case 0x18:
                        pass
                    case 0x1E:
                        self.i += self.v[x]
                    case 0x29:
                        self.i = self.v[x] * 5
                    case 0x33:
                        self.memory[self.i] = int(self.v[x] / 100)
                        self.memory[self.i + 1] = int((self.v[x] % 100) / 10)
                        self.memory[self.i + 2] = int(self.v[x] % 10)
                    case 0x55:
                        for rindex in range(x + 1):
                            self.memory[self.i + rindex] = self.v[rindex]
                    case 0x65:
                        for rindex in range(x + 1):
                            self.v[rindex] = self.memory[self.i + rindex]
                    case _: ...

            case _:
                raise Exception(f'Unknown opcode {opcode}')
        

