import tkinter as tk
import math


class Renderer(tk.Canvas):
    def __init__(self, master, scale=10, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.scale = scale

        self.cols = 64
        self.rows = 32

        self.config(bd=0, highlightthickness=0, bg='#000000',
            width=self.cols*self.scale, height=self.rows*self.scale)

        self.display = [0]*(self.rows * self.cols)
        self.display_buffer = [0] * (self.rows * self.cols)

        self.buffer = False

        self.render()
    
    def swap_buffers(self):
        self.display, self.display_buffer = self.display_buffer, self.display

    def set_pixel(self, x, y):
        if x > self.cols:
            x -= self.cols
        elif x < 0:
            x += self.cols
        
        if y > self.rows:
            y -= self.rows
        elif y < 0:
            y += self.rows

        pixelloc = x + (y * self.cols)
        self.display[pixelloc] ^= 1

        return not self.display[pixelloc]

    def clear(self):
        self.display = [0] * (self.rows * self.cols)

    def render(self):
        self.buffer = not self.buffer
        self.delete(str(self.buffer))

        for i in range(self.cols * self.rows):
            x = (i % self.cols) * self.scale - self.scale

            y = math.floor(i / self.cols) * self.scale

            if self.display[i]:
                self.create_rectangle(x, y, x+self.scale, y+self.scale, fill="#FFFFFF", tags=str(self.buffer))

        self.swap_buffers()

    def print_display(self):
        print(self.display)

    def test_render(self):
        self.set_pixel(0, 0)
        self.set_pixel(5, 2)
        self.render()

