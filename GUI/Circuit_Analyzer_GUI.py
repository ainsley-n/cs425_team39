# Import Packages
import tkinter as tk
from root import Root
from main_menu import MainMenu

# This is the main class for the GUI
# Frames for all screens are initialized
# Functionality for switching screens (Frames)
# Binding UI elements to other functionality in the program
#
# Some tkinter code is inspired by an example project:
#"How To Organize Multi-frame TKinter Application With MVC Pattern" by Nazmul Ahsan


class CircuitAnalyzerGUI():
    def __init__(self):
        self.root = Root("Circuit Analyzer")
        self.frames = {}
        self.current_frame = "main_menu"

        self._add_frame(MainMenu, "main_menu")
        self.frames["main_menu"].close_btn.config(command=self.root.destroy)


    def _add_frame(self, Frame, name):
        self.frames[name] = Frame(self.root)

    def switch(self, name):
        self.frames[self.current_frame].grid_forget()
        frame = self.frames[name]
        frame.grid(row=0, column=0, sticky="nsew")
        self.current_frame = name

    def start_mainloop(self):
        self.root.mainloop()


if __name__ == "__main__":
    analyzer = CircuitAnalyzerGUI()
    analyzer.switch("main_menu")
    analyzer.start_mainloop()
   