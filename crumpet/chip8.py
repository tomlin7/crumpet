import time
import tkinter as tk

from renderer import Renderer
from keyboard import Keyboard
from cpu import CPU


class Chip8(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.root = root
        
        self.renderer = Renderer(self)
        self.renderer.pack(fill=tk.BOTH)
        
        self.keyboard = Keyboard(self.root)
        self.cpu = CPU(self)

        self.fps = 60
        self.fps_interval = None
        
        self.init()

    def init(self):
        self.fps_interval = 1 / self.fps
   
        self.cpu.load_sprites()
        self.cpu.load_rom('roms/PONG')
        print("Loaded ROM")

        self.step()

    def step(self):
        start_time = time.time()

        self.cpu.cycle()
        self.renderer.swap_buffers()

        elapsed_time = time.time() - start_time
        remaining_time = max(0, self.fps_interval - elapsed_time)
        self.root.after(int(remaining_time * 1000), self.step)
