# From Example Program "How To Organize Multi-frame TKinter Application With MVC Pattern" by Nazmul Ahsan

from tkinter import Tk

class Root(Tk):
    def __init__(self, title: str, min_width: int, min_height: int, start_width: int | None=None, start_height: int | None=None):
        super().__init__()

        if start_width != None and start_height != None:
            self.geometry(f"{start_width}x{start_height}")
        self.minsize(width=min_width, height=min_height)
        self.title(title)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)