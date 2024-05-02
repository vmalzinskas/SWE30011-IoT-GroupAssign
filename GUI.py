import tkinter as tk
from msg import message

class VariableDisplayGUI:
    def __init__(self, root, mediator, target_temp):
        self.root = root
        self.mediator = mediator
        self.target_temp = target_temp
        self.current_temp = None
        # Set the size of the window
        self.root.geometry("300x200")  # Width x Height

        self.var1_label = tk.Label(root, text="Target temperature: " + str(self.target_temp))
        self.var1_label.pack()

        # Entry widget to enter a new temperature
        self.temp_entry = tk.Entry(root)
        self.temp_entry.pack()

        self.update_button = tk.Button(root, text="Update Temp", command=self.update_variables)
        self.update_button.pack()



    def send_to_mediator(self):
        self.mediator.receive_message(message('controller', channel='set_temp', data=self.target_temp))

    def update_variables(self):
        self.target_temp = self.temp_entry.get()
        self.var1_label.config(text="Target temperature: " + str(self.target_temp))
        self.send_to_mediator()

