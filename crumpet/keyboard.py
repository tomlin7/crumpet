class Keyboard:
    def __init__(self, text):
        self.text = text

        self.KEYMAP = {
            '1': 0x1, # 1
            '2': 0x2, # 2
            '3': 0x3, # 3
            '4': 0xc, # 4
            'Q': 0x4, # Q
            'W': 0x5, # W
            'E': 0x6, # E
            'R': 0xD, # R
            'A': 0x7, # A
            'S': 0x8, # S
            'D': 0x9, # D
            'F': 0xE, # F
            'Z': 0xA, # Z
            'X': 0x0, # X
            'C': 0xB, # C
            'V': 0xF  # V
        }

        self.keys_pressed = {}
        self.on_next = None
      
        self.text.bind("<KeyPress>", self.key_down)
        self.text.bind("<KeyRelease>", self.key_up)

    def key_down(self, e):
        if key := self.KEYMAP.get(e.keysym, None):
            self.keys_pressed[key] = True

            if self.on_next != None:
                self.on_next(int(key, base=16))
                self.on_next = None

        return "break"

    def key_up(self, e):
        if key := self.KEYMAP.get(e.keysym, None):
            self.keys_pressed[key] = False


    def is_key_pressed(self, keycode):
        return self.keys_pressed.get(keycode, None)

