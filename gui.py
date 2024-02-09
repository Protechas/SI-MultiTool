# gui.py
import os
import fitz
import string
import re
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import time
import threading
from tkinter import ttk
import csv
import shutil
import PyPDF2
import sys
from cx_Freeze import setup, Executable
import Win
import yb

class BabyHipsGUI:
    def __init__(self, root):
        def move_and_split_files(self):
            try:
                oversized_files = []  # List to store information about oversized PDF files
                for root, dirs, files in os.walk(self.parent_directory_path):
                    for file_name in files:
                        file_path = os.path.join(root, file_name)
                        try:
                            if file_name.lower().endswith(".pdf"):
                                if any(file_name.lower().endswith(f"part-{i}.pdf") for i in range(1, 5)):
                                    self.compress_pdf(file_path)
                                else:
                                    self.compress_pdf(file_path)
                                    file_size_kb = os.path.getsize(file_path) / 1024
                                    if file_size_kb > 1400:
                                        year = file_path.split(os.sep)[-3]
                                        make = file_path.split(os.sep)[-4]
                                        model = file_path.split(os.sep)[-2]
                                        system = "N/A"  # You may want to extract the system information as well
                                        file_size = f"{file_size_kb:.2f} KB"
                                        oversized_files.append({"Year": year, "Make": make, "Model": model, "System": system, "File size": file_size})
                                        new_folder_path = os.path.join(os.path.dirname(file_path), os.path.splitext(file_name)[0])
                                        new_file_path = os.path.join(new_folder_path, file_name)
                                        if os.path.exists(new_folder_path):
                                            os.remove(new_file_path)
                        except Exception as e:
                            print(f"Error while processing {file_path}: {str(e)}")
                csv_report_path = os.path.join(self.output_path_entry.get(), "oversized_files_report.csv")
                if not oversized_files:
                    with open(csv_report_path, 'w', newline='', encoding='utf-8') as csv_file:
                        csv_file.write("NO OVERSIZED PDF FILES")
                    print("No oversized PDF files found.")
                else:
                    with open(csv_report_path, 'w', newline='', encoding='utf-8') as csv_file:
                        fieldnames = ["Year", "Make", "Model", "System", "File size"]
                        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerows(oversized_files)
                    print("File moving, splitting, and compressing complete.")
                    print(f"Oversized PDF files report written to: {csv_report_path}")
            except Exception as e:
                print(f"Error while moving and splitting PDF files: {str(e)}")

        def compress_pdf(self, input_path):
            try:
                file_size_kb = os.path.getsize(input_path) / 1024  # Calculate file size in kilobytes
                if file_size_kb > 1400:
                    folder_name = os.path.splitext(os.path.basename(input_path))[0]
                    folder_path = os.path.join(os.path.dirname(input_path), folder_name)
                    os.makedirs(folder_path, exist_ok=True)
                    new_file_path = os.path.join(folder_path, os.path.basename(input_path))
                    shutil.move(input_path, new_file_path)
                    output_path = os.path.join(folder_path, f"{folder_name}_compressed.pdf")
                else:
                    output_path = input_path  # Use the same input path as the output path
                    doc = fitz.open(input_path)  # Open the document for compression
                    output_path = os.path.join(os.path.dirname(input_path), f"{os.path.splitext(os.path.basename(input_path))[0]}_compressed.pdf")
                    new_doc = fitz.open()  # Open a new document for compressed content
                    for page_num in range(len(doc)):
                        try:
                            new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num, rotate=0)
                        except Exception as e:
                            print(f"Error while compressing page {page_num + 1} of {input_path}: {str(e)}")
                    doc.close()  # Close the original document
                    new_doc.save(output_path, garbage=4, deflate=True, clean=True)
                    new_doc.close()  # Close the new document
            except Exception as e:
                print(f"Error while compressing PDF: {str(e)}")

        def compress_pdfs(self):
            parent_directory_path = self.input_path_entry.get()
            output_csv_path = self.output_csv_path
            if not parent_directory_path:
                messagebox.showerror("Error", "Please select an input directory.")
                return
            compressed_files = []
            total_files = sum([len(files) for root, dirs, files in os.walk(parent_directory_path) if files])
            processed_files = 0
            self.start_time = time.time()  # Store the start time
            for root, dirs, files in os.walk(parent_directory_path):
                for file in files:
                    if file.endswith('.pdf'):
                        input_path = os.path.join(root, file)
                        for _ in range(3):
                            try:
                                self.compress_pdf(input_path)
                                break  # Break the retry loop if successful
                            except Exception as e:
                                print(f"Error while compressing PDF: {str(e)}")
                                time.sleep(1)
                        processed_files += 1
                        total_percentage = (processed_files / total_files) * 100
                        elapsed_time = time.time() - self.start_time
                        remaining_time = (elapsed_time / total_percentage) * (100 - total_percentage)
                        print(f"Compressing: {file}. Total Progress: {total_percentage:.2f}%")
                        self.progress_bar['value'] = total_percentage
                        self.percentage_label.config(text=f"{total_percentage:.2f}%")
                        self.root.update_idletasks()
                        time.sleep(0.1)

                        # Compress the PDF file before moving and splitting
                        self.compress_pdf(input_path)
                        
            self.move_and_split_files()
            print(f'Compression and file moving/splitting complete.')

        def split_pdf(self, input_file, output_folder):
            try:
                file_size_kb = os.path.getsize(input_file) / 1024  # Calculate file size in kilobytes
                max_part_size_kb = 1300  # Adjust this value based on your requirement
                if file_size_kb > max_part_size_kb:
                    input_pdf = fitz.open(input_file)
                    base_filename = os.path.splitext(os.path.basename(input_file))[0]
                    os.makedirs(output_folder, exist_ok=True)
                    part_num = 1
                    current_part_size = 0
                    current_part = fitz.open()
                    for page_num in range(input_pdf.page_count):
                        if current_part_size > 0:
                            output_file = os.path.join(output_folder, f"{base_filename} part-{part_num}.pdf")
                            current_part.save(output_file)
                            self.compress_pdf(output_file)  # Compress the last split file
                            current_part.close()  # Close the current_part
                        part_num += 1
                        current_part_size = 0
                        current_part = fitz.open()
                    input_pdf.close()
                    os.remove(input_file)
            except Exception as e:
                print(f"Error while splitting PDF: {str(e)}")

        def pull_from(self):
            directory_path = filedialog.askdirectory()
            self.input_path_entry.delete(0, tk.END)
            self.input_path_entry.insert(0, directory_path)
            self.parent_directory_path = directory_path

        def create_in(self):
            directory_path = filedialog.askdirectory()
            self.output_path_entry.delete(0, tk.END)
            self.output_path_entry.insert(0, directory_path)
            self.output_csv_path = os.path.join(directory_path, "Extracted Highlights.csv")

        def closest_color(self, color):
            color = np.array(color)
            distances = {np.linalg.norm(color - YELLOW): "Yellow", np.linalg.norm(color - BLUE): "Blue"}
            return distances[min(distances)]

        def extract_info_from_path(self, file_path):
            _, filename = os.path.split(file_path)
            matches = re.findall(r'\b\d+\b|\b[A-Z][a-z]*\b', filename)
            year = matches[0] if matches else "N/A"
            make = matches[1] if len(matches) > 1 else "N/A"
            model_match = re.search(r'\b[A-Z][a-zA-Z0-9 ]*\b', filename)
            model = model_match.group() if model_match else "N/A"
            model = model.replace(make, '').strip()
            match = re.search(r'\((.*?)\)', filename)
            system = match.group(1) if match else "N/A"
            return year, make, model, system

        def extract_highlights(self, file_path):
            try:
                doc = fitz.open(file_path)
            except:
                print(f"Could not open {file_path}, skipping...")
                return [{"Year": "N/A", "Make": "N/A", "Model": "N/A", "System": "N/A", "Text": "Could not open file.", "HighlightColor": "N/A"}]
            num_pages = len(doc)
            _, filename = os.path.split(file_path)
            match = re.search(r'\((.*?)\)', filename)
            system = match.group(1) if match else "N/A"
            year, make, model, _ = self.extract_info_from_path(file_path)
            highlights = []
            for page_num in range(num_pages):
                page = doc[page_num]
                annotations = page.annots()
                for annotation in annotations:
                    if annotation.type[1] == "Highlight":
                        color_classification = self.closest_color(annotation.colors["stroke"])
                        highlight_rect = fitz.Rect(annotation.rect)
                        words = page.get_text("words", clip=highlight_rect)
                        highlighted_text = ' '.join([word[4] for word in words])
                        printable = set(string.printable)
                        highlighted_text = "".join(filter(lambda x: x in printable, highlighted_text))
                        highlight = {
                            "Year": year,
                            "Make": make,
                            "Model": model,
                            "System": system,
                            "Text": highlighted_text,
                            "HighlightColor": color_classification
                        }
                        highlights.append(highlight)
            return highlights

        def count_files_in_make(self, make_path):
            count = 0
            years = [os.path.join(make_path, year) for year in os.listdir(make_path) if os.path.isdir(os.path.join(make_path, year))]
            for year in years:
                models = [os.path.join(year, model) for model in os.listdir(year) if os.path.isdir(os.path.join(year, model))]
                for model in models:
                    for root, dirs, files in os.walk(model):
                        for file in files:
                            if file.endswith(".pdf"):
                                count += 1
            return count

        def extract_highlights_action(self):
            input_path = self.input_path_entry.get()
            output_csv_path = self.output_csv_path
            if not input_path:
                messagebox.showerror("Error", "Please select an input directory.")
                return
            makes = [os.path.join(input_path, make) for make in os.listdir(input_path) if os.path.isdir(os.path.join(input_path, make))]
            total_files = sum([self.count_files_in_make(make) for make in makes])
            processed_files = 0
            self.process_directory(input_path, output_csv_path)

        def process_directory(self, parent_directory_path, output_csv_path):
            all_highlights = []
            makes = [os.path.join(parent_directory_path, make) for make in os.listdir(parent_directory_path) if os.path.isdir(os.path.join(parent_directory_path, make))]
            total_makes = len(makes)
            total_files = sum([self.count_files_in_make(make) for make in makes])
            processed_files = 0
            for idx, make in enumerate(makes):
                make_files = self.count_files_in_make(make)
                if make_files == 0:
                    print(f"Skipping make {idx+1}/{total_makes} (No PDF files found)...")
                    continue
                processed_make_files = 0
                print(f"Processing make {idx+1}/{total_makes} ({make_files} files)...")
                years = [os.path.join(make, year) for year in os.listdir(make) if os.path.isdir(os.path.join(make, year))]
                for year in years:
                    models = [os.path.join(year, model) for model in os.listdir(year) if os.path.isdir(os.path.join(year, model))]
                    for model in models:
                        for root, dirs, files in os.walk(model):
                            for file in files:
                                if file.endswith(".pdf"):
                                    file_path = os.path.join(root, file)
                                    highlights = self.extract_highlights(file_path)
                                    all_highlights.extend(highlights)
                                    processed_files += 1
                                    processed_make_files += 1
                make_percentage = (processed_make_files / make_files) * 100
                total_percentage = (processed_files / total_files) * 100
                print(f"Finished Processing: {make}. Make Progress: {make_percentage:.2f}%")
                print(f"Total Progress: {total_percentage:.2f}%")
            num_highlights = len(all_highlights)
            print(f"Total highlights found: {num_highlights}")
            if num_highlights > 0:
                with open(output_csv_path, "w", newline="", encoding="utf-8") as csv_file:  # add encoding="utf-8"
                    fieldnames = ["Year", "Make", "Model", "System", "Text", "HighlightColor"]
                    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(all_highlights)
                print(f"Highlights saved to {output_csv_path}")
        def copy_pages(self, file_path, color):
            try:
                doc = fitz.open(file_path)
            except:
                print(f"Could not open {file_path}, skipping...")
                return
            num_pages = len(doc)
            for page_num in range(num_pages):
                page = doc[page_num]
                annotations = page.annots()
                for annotation in annotations:
                    if annotation.type[1] == "Highlight":
                        highlight_color = closest_color(annotation.colors["stroke"])
                        if highlight_color == color:
                            highlight_rect = fitz.Rect(annotation.rect)
                            words = page.get_text("words", clip=highlight_rect)
                            highlighted_text = ' '.join([word[4] for word in words])
                            printable = set(string.printable)
                            highlighted_text = ''.join(filter(lambda x: x in printable, highlighted_text))
                            output_file_path = os.path.join(self.output_path_entry.get(), f"{os.path.splitext(os.path.basename(file_path))[0]}_{highlight_color}.pdf")
                            new_doc = fitz.open()
                            new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
                            new_doc.save(output_file_path)
            doc.close()

        def copy_yellow_pages(self):
            makes = [os.path.join(self.input_path_entry.get(), make) for make in os.listdir(self.input_path_entry.get()) if os.path.isdir(os.path.join(self.input_path_entry.get(), make))]
            for make in makes:
                years = [os.path.join(make, year) for year in os.listdir(make) if os.path.isdir(os.path.join(make, year))]
                for year in years:
                    models = [os.path.join(year, model) for model in os.listdir(year) if os.path.isdir(os.path.join(year, model))]
                    for model in models:
                        for root, dirs, files in os.walk(model):
                            for file in files:
                                if file.endswith(".pdf"):
                                    file_path = os.path.join(root, file)
                                    self.copy_pages(file_path, "Yellow")
            messagebox.showinfo("Copy Yellow Highlights", "Yellow highlighted pages copied successfully!")

        def copy_blue_pages(self):
            makes = [os.path.join(self.input_path_entry.get(), make) for make in os.listdir(self.input_path_entry.get()) if os.path.isdir(os.path.join(self.input_path_entry.get(), make))]
            for make in makes:
                years = [os.path.join(make, year) for year in os.listdir(make) if os.path.isdir(os.path.join(make, year))]
                for year in years:
                    models = [os.path.join(year, model) for model in os.listdir(year) if os.path.isdir(os.path.join(year, model))]
                    for model in models:
                        for root, dirs, files in os.walk(model):
                            for file in files:
                                if file.endswith(".pdf"):
                                    file_path = os.path.join(root, file)
                                    self.copy_pages(file_path, "Blue")
            messagebox.showinfo("Copy Blue Highlights", "Blue highlighted pages copied successfully!")

        def copy_yb_pages(self):
            makes = [os.path.join(self.input_path_entry.get(), make) for make in os.listdir(self.input_path_entry.get()) if os.path.isdir(os.path.join(self.input_path_entry.get(), make))]
            for make in makes:
                years = [os.path.join(make, year) for year in os.listdir(make) if os.path.isdir(os.path.join(make, year))]
                for year in years:
                    models = [os.path.join(year, model) for model in os.listdir(year) if os.path.isdir(os.path.join(year, model))]
                    for model in models:
                        for root, dirs, files in os.walk(model):
                            for file in files:
                                if file.endswith(".pdf"):
                                    file_path = os.path.join(root, file)
                                    has_yellow = False
                                    has_blue = False
                                    doc = fitz.open(file_path)
                                    num_pages = len(doc)
                                    for page_num in range(num_pages):
                                        page = doc[page_num]
                                        annotations = page.annots()
                                        for annotation in annotations:
                                            if annotation.type[1] == "Highlight":
                                                annotation_color = closest_color(annotation.colors["stroke"])
                                                if annotation_color == "Yellow":
                                                    has_yellow = True
                                                elif annotation_color == "Blue":
                                                    has_blue = True
                                                if has_yellow and has_blue:
                                                    output_file_path = os.path.join(self.output_path_entry.get(), f"{os.path.splitext(os.path.basename(file_path))[0]}_YB.pdf")
                                                    new_doc = fitz.open()
                                                    new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
                                                    for other_page_num in range(num_pages):
                                                        other_page = doc[other_page_num]
                                                        other_annotations = other_page.annots()
                                                        for other_annotation in other_annotations:
                                                            if other_annotation.type[1] == "Highlight" and closest_color(other_annotation.colors["stroke"]) == "Blue":
                                                                new_doc.insert_pdf(doc, from_page=other_page_num, to_page=other_page_num)
                                                                break
                                                    new_doc.save(output_file_path)
                                                    break
                                        if has_yellow and has_blue:
                                            break
                                    doc.close()
            messagebox.showinfo("Copy Y/B Highlights", "Pages with both yellow and blue highlights copied successfully!")

        def pull_library(module):
            module.init__module()

            if __name__ == "__main__":
                pull_library(yb)

        def run(self):
            self.root.mainloop()