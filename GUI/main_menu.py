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

        self.generate_btn = Button(self, text="Generate Circuit", width=25, height=5)
        self.generate_btn.grid(row=1, column=0, padx=10, pady=10)

        self.load_btn = Button(self, text="Load Circuit", width=25, height=5)
        self.load_btn.grid(row=1, column=1, padx=10, pady=10)

        self.create_btn = Button(self, text="Create Circuit", width=25, height=5)
        self.create_btn.grid(row=1, column=2, padx=10, pady=10)

        self.close_btn = Button(self, text="Close")
        self.close_btn.grid(row=2, column=2, padx=10, pady=10, sticky="se")