class Keyboard:
    def __init__(self, text):
        self.text = text

        self.KEYMAP = {
            '1': 0x1, # 1
            '2': 0x2, # 2
            '3': 0x3, # 3
            '4': 0xc, # 4
            'q': 0x4, # Q
            'w': 0x5, # W
            'e': 0x6, # E
            'r': 0xD, # R
            'a': 0x7, # A
            's': 0x8, # S
            'd': 0x9, # D
            'f': 0xE, # F
            'z': 0xA, # Z
            'x': 0x0, # X
            'c': 0xB, # C
            'v': 0xF  # V
        }

        self.keys_pressed = {}
        self.on_next = None
      
        self.text.bind("<KeyPress>", self.key_down)
        self.text.bind("<KeyRelease>", self.key_up)

    def key_down(self, e):
        if key := self.KEYMAP.get(e.keysym, None):
            print(e.keysym, key)
            self.keys_pressed[key] = True

            if self.on_next != None:
                print(key)
                self.on_next(int(key, base=16))
                self.on_next = None
        return "break"

    def key_up(self, e):
        if key := self.KEYMAP.get(e.keysym, None):
            self.keys_pressed[key] = False

    def is_key_pressed(self, keycode):
        return self.keys_pressed.get(keycode, None)
