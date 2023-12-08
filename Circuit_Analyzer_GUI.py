# Import Packages
import tkinter as tk
from GUI.root import Root
from GUI.error_window import ErrorWindow
from GUI.main_menu import MainMenu

import Circuit_Analyzer

# This is the main class for the GUI
# Frames for all screens are initialized
# Functionality for switching screens (Frames)
# Binding UI elements to other functionality in the program
#
# Some tkinter code is inspired by an example project:
#"How To Organize Multi-frame TKinter Application With MVC Pattern" by Nazmul Ahsan


class CircuitAnalyzerGUI():
    def __init__(self):
        self.root = Root("Circuit Analyzer", 400, 250, 500, 300)
        self.frames = {}
        self.current_frame = "main_menu"

        self._add_frame(MainMenu, "main_menu")
        self.main_menu_controller = MainMenuController(self.frames["main_menu"], self.root)
        

    def _add_frame(self, Frame, name):
        self.frames[name] = Frame(self.root)

    def switch(self, name):
        self.frames[self.current_frame].grid_forget()
        frame = self.frames[name]
        frame.grid(row=0, column=0, sticky="nsew")
        self.current_frame = name

    def start_mainloop(self):
        self.root.mainloop()

class MainMenuController():
    def __init__(self, frame, root):
        frame.close_btn.config(command=root.destroy)
        frame.generate_btn.config(command=lambda: ErrorWindow("Feature Not Yet Implemented", root))
        frame.create_btn.config(command=lambda: ErrorWindow("Feature Not Yet Implemented", root))

if __name__ == "__main__":
    analyzer = CircuitAnalyzerGUI()
    analyzer.switch("main_menu")
    analyzer.start_mainloop()
   