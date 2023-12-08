from tkinter import Label, Button, Toplevel

# Class to generate an error window on demand

class ErrorWindow():
    def __init__(self, message, master):
        self.window = Toplevel()
        self.window.title("Error")
        
        self.message_label = Label(self.window, text=message)
        self.message_label.pack(padx=10, pady=10)

        self.close_button = Button(self.window, text="close", command=self.window.destroy)
        self.close_button.pack(padx=10, pady=10)
        
        self.window.resizable(False, False)

        #Found these lines of code online
        #Pauses main window while error window is active
        self.window.transient(master) #set to be on top of the main window
        self.window.grab_set() #hijack all commands from the master (clicks on the main window are ignored)
        master.wait_window(self.window) #pause anything on the main window until this one closes
    