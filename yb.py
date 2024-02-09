# yb.py
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from cx_Freeze import setup, Executable

def init__module():
    YELLOW = np.array([1.0, 1.0, 0.0])
    BLUE = np.array([0.0, 0.0, 1.0])

    def closest_color(color):
        color = np.array(color)
        distances = {np.linalg.norm(color - YELLOW): "Yellow", np.linalg.norm(color - BLUE): "Blue"}
        return distances[min(distances)]
    
    print("Initializing yb module")