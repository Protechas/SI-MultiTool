# Win.py
import tkinter as tk
from tkinter import ttk
import gui

class BabyHipsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("S.I. Multi-Tool")
        self.parent_directory_path = None
        self.output_csv_path = None
        self.output_directory = None
        self.start_time = None
        self.total_time_value = tk.StringVar()
        self.total_time_value.set("N/A")

        self.root.configure(bg='sky blue')

        self.input_frame = tk.Frame(root)
        self.input_frame.pack(padx=10, pady=10)

        self.output_frame = tk.Frame(root)
        self.output_frame.pack(padx=10, pady=10)

        self.extract_frame = tk.Frame(root)
        self.extract_frame.pack(padx=10, pady=10)

        self.compress_frame = tk.Frame(root)
        self.compress_frame.pack(padx=10, pady=10)

        self.progress_frame = tk.Frame(root)
        self.progress_frame.pack(padx=10, pady=10)

        self.copy_frame = tk.Frame(root)
        self.copy_frame.pack(padx=10, pady=10)

        self.input_path_label = tk.Label(self.input_frame, text="Input Path:")
        self.input_path_label.grid(row=0, column=0)
        self.input_path_entry = tk.Entry(self.input_frame)
        self.input_path_entry.grid(row=0, column=1)
        self.pull_from_button = tk.Button(self.input_frame, text="Pull From", command=self.pull_from)
        self.pull_from_button.grid(row=0, column=2)

        self.output_path_label = tk.Label(self.output_frame, text="Output Path:")
        self.output_path_label.grid(row=0, column=0)
        self.output_path_entry = tk.Entry(self.output_frame)
        self.output_path_entry.grid(row=0, column=1)
        self.create_in_button = tk.Button(self.output_frame, text="Create In", command=self.create_in)
        self.create_in_button.grid(row=0, column=2)

        self.compress_button = tk.Button(self.compress_frame, text="Compress Files", command=self.compress_pdfs)
        self.compress_button.grid(row=0, column=0)

        self.progress_label = tk.Label(self.progress_frame, text="Progress:")
        self.progress_label.grid(row=0, column=0)
        self.progress_bar = ttk.Progressbar(self.progress_frame, length=200)
        self.progress_bar.grid(row=0, column=1)
        self.percentage_label = tk.Label(self.progress_frame, text="")
        self.percentage_label.grid(row=0, column=2)

        self.estimated_time_label = tk.Label(self.progress_frame, text="Estimated Time Remaining:")
        self.estimated_time_label.grid(row=1, column=0)
        self.estimated_time_label_value = tk.Label(self.progress_frame, textvariable=self.total_time_value)
        self.estimated_time_label_value.grid(row=1, column=1)

        self.copy_yellow_button = tk.Button(self.copy_frame, text="Copy Yellow Highlights", command=self.copy_yellow_pages)
        self.copy_yellow_button.grid(row=0, column=0)
        self.copy_blue_button = tk.Button(self.copy_frame, text="Copy Blue Highlights", command=self.copy_blue_pages)
        self.copy_blue_button.grid(row=0, column=1)
        self.copy_yb_button = tk.Button(self.copy_frame, text="Copy Y/B Highlights", command=self.copy_yb_pages)
        self.copy_yb_button.grid(row=0, column=2)
        self.center_window()

    def center_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - self.root.winfo_reqwidth()) // 2
        y = (screen_height - self.root.winfo_reqheight()) // 2
        self.root.geometry("+{}+{}".format(x, y))

    def pull_library(self, module):
        module.init__module()

if __name__ == "__main__":
    root = tk.Tk()
    app = BabyHipsGUI(root)
    app.pull_library(gui)
    app.run()
