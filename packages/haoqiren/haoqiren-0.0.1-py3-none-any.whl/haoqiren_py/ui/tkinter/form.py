from tkinter import *
from .tkinterhelper import *

import os


class Form:
    def __init__(self, overrideredirect=False, center=True, title="Form", width=400, height=300, left=0, top=0):
        self.root = Tk()
        if not overrideredirect:
            self.root.title(title)
            if center:
                set_window_center(self.root, width, height)
            else:
                self.root.geometry(get_geometry(width, height, left, top))
        else:
            set_wm_overrideredirect(self.root, overrideredirect)
            if center:
                set_window_center(self.root, width, height, 0, 0)
            else:
                self.root.geometry(get_geometry(width, height, left, top))

    def mainloop(self):
        self.root.mainloop()
