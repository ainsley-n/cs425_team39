from tkinter import Frame, Label, Button

# This class defines the Main Menu as a Tk Frame 

class MainMenu(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=2)
        self.grid_rowconfigure(2, weight=1)

        self.header = Label(self, text="Welcome to Circuit Analyzer!")
        self.header.grid(row=0, column=1, padx=10, pady=10, sticky="ew")