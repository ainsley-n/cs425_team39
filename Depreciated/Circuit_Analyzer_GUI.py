# Import Packages
import tkinter as tk
import tkinter.messagebox as mb
from tkinter import filedialog as fd
from GUI.root import Root
from GUI.main_menu import MainMenu
from GUI.load_menu import LoadMenu
from GUI.circuit_analysis import CircuitAnalysis

from Circuit_Analyzer import create_circuit_from_file
from lcapy import Circuit

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
        self.current_filename = ""
        self.current_circuit = Circuit()

        self._add_frame(MainMenu, "main_menu")
        self.main_menu_controller = MainMenuController(self.frames["main_menu"], self)

        self._add_frame(LoadMenu, "load_menu")
        self.load_menu_controller = LoadMenuController(self.frames["load_menu"], self)

        self._add_frame(CircuitAnalysis, "circuit_analysis")
        self.circuit_analysis_controller = CircuitAnalysisController(self.frames["circuit_analysis"], self)
        

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
    def __init__(self, frame, controller):
        frame.close_btn.config(command=controller.root.destroy)
        frame.generate_btn.config(command = unimplemented)
        frame.create_btn.config(command = unimplemented)
        frame.load_btn.config(command=lambda: controller.switch("load_menu"))

class LoadMenuController():
    def __init__(self, frame, controller):
        self.filename = tk.StringVar()
        frame.close_btn.config(command=controller.root.destroy)
        frame.back_btn.config(command=lambda : controller.switch("main_menu"))
        frame.load_btn.config(command = lambda: 
                              self.load_circuit(self.filename.get(), controller))
        frame.file_entry.config(textvariable = self.filename)
        frame.file_btn.config(command = self.select_file)

    def load_circuit(self, filename, controller):
        controller.current_filename = filename
        try:
            controller.current_circuit = create_circuit_from_file(filename)
        except FileNotFoundError:
            mb.showerror(
                title="File Not Found",
                message="The file you entered does not exist. Please try again."
            )
        except ValueError:
            mb.showerror(
                title="Error",
                message="An error occured.\nThis file may not contain a netlist. Please try again."
            )
        else:
            controller.circuit_analysis_controller.update_image()
            controller.switch("circuit_analysis")

    def select_file(self):
        filetypes = (
            ('netlist files', '*.net'),
            ('All files', '*.*')
        )

        self.filename.set(fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes))
        
class CircuitAnalysisController():
    def __init__(self, frame, controller):
        self.frame = frame
        self.controller = controller
        frame.back_btn.config(command=lambda : controller.switch("main_menu"))

    def update_image(self):
        self.controller.current_circuit.draw('temp/circuit.png')
        image = tk.PhotoImage(file='temp/circuit.png')
        self.frame.image_label.config(image=image)
        self.frame.image_label.image = image
def unimplemented():
    mb.showwarning(
                title="Warning",
                message="This feature has not been implemented yet."
            )



if __name__ == "__main__":
    analyzer = CircuitAnalyzerGUI()
    analyzer.switch("main_menu")
    analyzer.start_mainloop()
   