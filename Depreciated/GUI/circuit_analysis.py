from tkinter import Frame, Label, Button, Entry

# This class defines the Main Menu as a Tk Frame 

class CircuitAnalysis(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=2)
        self.grid_rowconfigure(2, weight=0)

        self.header = Label(self, text="Analyzing the following circuit:", padx=10, pady=10)
        self.header.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.back_btn = Button(self, text="Back")
        self.back_btn.grid(row=2, column=0, padx=10, pady=10, sticky="sw")

        self.image_label = Label(self)
        self.image_label.grid(row=1, column=0, padx=10, pady=10)

