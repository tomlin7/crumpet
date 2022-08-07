import tkinter as tk
import ctypes as ct

from chip8 import Chip8


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_titlebar() 

        self.base = Chip8(self)
        self.base.pack(fill=tk.BOTH)

    def config_titlebar(self):
        self.update()

        hwnd = ct.windll.user32.GetParent(self.winfo_id())
        ct.windll.dwmapi.DwmSetWindowAttribute(
                hwnd, 20, ct.byref(ct.c_int(2)),
                ct.sizeof(ct.c_int(2)))
        
if __name__ == '__main__':
    app = App()
    app.mainloop()

