# main.py
import tkinter as tk
import Win
import gui

def pull_library(module):
    module.init__module()

if __name__ == "__main__":
    root = tk.Tk()

    # Initialize and set up the GUI instance
    gui_instance = gui.BabyHipsGUI(root)

    # Initialize and set up the Win instance
    win_instance = Win.BabyHipsGUI(root)
    win_instance.pull_library(gui_instance)

    root.mainloop()
