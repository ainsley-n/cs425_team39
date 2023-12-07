# From Example Program "How To Organize Multi-frame TKinter Application With MVC Pattern" by Nazmul Ahsan

from tkinter import Tk

class Root(Tk):
    def __init__(self, title):
        super().__init__()

        start_width = 500
        min_width = 400
        start_height = 300
        min_height = 250

        self.geometry(f"{start_width}x{start_height}")
        self.minsize(width=min_width, height=min_height)
        self.title(title)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)