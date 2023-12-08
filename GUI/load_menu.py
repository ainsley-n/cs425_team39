from tkinter import Frame, Label, Button

# This class defines the Main Menu as a Tk Frame 

class LoadMenu(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=1)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=2)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=2)

        self.header = Label(self, text="Load a text file containing a SPICE netlist:", padx=10, pady=10)
        self.header.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        self.load_btn = Button(self, text="Load Circuit")
        self.load_btn.grid(row=2, column=1, padx=10, pady=10)

        self.back_btn = Button(self, text="Back")
        self.back_btn.grid(row=3, column=0, padx=10, pady=10, sticky="sw")

        self.close_btn = Button(self, text="Close")
        self.close_btn.grid(row=3, column=2, padx=10, pady=10, sticky="se")
        
        self.input_label = Label(self, text="File Path:", padx=10, pady=10)
        self.input_label.grid(row=1, column=0, padx=0, pady=0, sticky="e")