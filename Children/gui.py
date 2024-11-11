import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
from encryptionhandler import *

# Global Variables
entries = []
tempentries = {}

class WelcomePage:
    def __init__(self, root):
        # Frame and widgets for Welcome Page
        self.mainframe = ttk.Frame(root, padding="15 15 15 15")
        label = ttk.Label(self.mainframe, text="Welcome to HoneyDefense", font=("Helvetica", 16))
        button = ttk.Button(self.mainframe, text="Next Page", command=self.next_page)
        separator = ttk.Separator(self.mainframe, orient="horizontal")
        
        # Layout configuration
        self.mainframe.pack(expand=True, fill="both")
        label.grid(column=1, row=0, pady=(10, 10))
        separator.grid(column=0, row=1, columnspan=4, sticky="ew", pady=(10, 10))
        button.grid(column=3, row=3, padx=(10, 10), pady=(10, 10))
        
        # Column and row weights for spacing
        for i in range(4):
            self.mainframe.columnconfigure(i, weight=1)
        for i in range(4):
            self.mainframe.rowconfigure(i, weight=1)

    def next_page(self):
        self.mainframe.destroy()
        AddFiles(root)

class AddFiles:
    def __init__(self, root):
        # Frame for AddFiles page
        self.mainframe = ttk.Frame(root, padding="15 15 15 15")
        self.mainframe.pack(expand=True, fill="both")

        # Label for the Add Files page title
        label = ttk.Label(self.mainframe, text="Welcome to Add Files Page", font=("Helvetica", 16))
        label.grid(column=0, row=0, columnspan=2, sticky="w", pady=(5, 15))

        # Button to select directory
        self.select_dir_button = ttk.Button(self.mainframe, text="Select Directory", command=self.askfiledirectory)
        self.select_dir_button.grid(column=0, row=1, pady=(10, 10), sticky="w")

        # Listbox for file type selection
        self.file_type_label = ttk.Label(self.mainframe, text="Select File Type:", font=("Helvetica", 12))
        self.file_type_label.grid(column=0, row=2, sticky="w", pady=(5, 5))

        self.file_type_listbox = tk.Listbox(self.mainframe, height=4, selectmode="single", exportselection=False, font=("Helvetica", 12))
        self.file_type_listbox.insert(1, "Text File")
        self.file_type_listbox.insert(2, "PDF")
        self.file_type_listbox.insert(3, "Image")
        self.file_type_listbox.insert(4, "Video")
        self.file_type_listbox.grid(column=1, row=2, sticky="ew", padx=(10, 10))

        # Entry for filename
        self.filename_label = ttk.Label(self.mainframe, text="Enter Filename:", font=("Helvetica", 12))
        self.filename_label.grid(column=0, row=3, sticky="w", pady=(5, 5))

        self.filename_entry = ttk.Entry(self.mainframe, width=30, font=("Helvetica", 12))
        self.filename_entry.grid(column=1, row=3, sticky="ew", padx=(10, 10))

        # Back, Add Another File, and Next buttons
        self.back_button = ttk.Button(self.mainframe, text="Back", command=self.go_back)
        self.back_button.grid(column=0, row=4, pady=(20, 0), sticky="w")

        self.add_another_button = ttk.Button(self.mainframe, text="Add Another File", command=self.add_another_file)
        self.add_another_button.grid(column=1, row=4, pady=(20, 0), sticky="w")

        self.next_button = ttk.Button(self.mainframe, text="Next", command=self.save_and_next)
        self.next_button.grid(column=1, row=5, pady=(10, 0), sticky="e")

        # Column and row weights for spacing
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.columnconfigure(1, weight=2)
        for i in range(6):
            self.mainframe.rowconfigure(i, weight=1)

    def askfiledirectory(self):
        # Function to ask for directory
        directory = filedialog.askdirectory()
        if directory:
            print("Selected directory:", directory)
            tempentries["Directory"] = directory

    def go_back(self):
        # Return to the WelcomePage
        self.mainframe.destroy()
        WelcomePage(root)

    def add_another_file(self):
        # Save the current entry and reset fields for another file entry
        file_type = self.file_type_listbox.get(tk.ACTIVE)
        filename = self.filename_entry.get().strip()

        if tempentries.get("Directory") and file_type and filename:
            tempentries['FileType'] = file_type
            tempentries['FileName'] = filename
            entries.append(tempentries.copy())
            tempentries.clear()
            print("Added entry:", entries[-1])

            # Clear fields for next entry
            self.filename_entry.delete(0, tk.END)
            self.file_type_listbox.selection_clear(0, tk.END)
        else:
            print("Please ensure Directory, File Type, and Filename are provided.")

    def save_and_next(self):
        # Save current entry, then navigate to SummaryPage
        if tempentries.get("Directory") or self.file_type_listbox.curselection() or self.filename_entry.get().strip():
            self.add_another_file()  # Save current entry if any fields are filled
        print("Entries:", entries)
        
        self.mainframe.destroy()
        SummaryPage(root)

class SummaryPage:
    def __init__(self, root):
        # Frame for SummaryPage
        self.mainframe = ttk.Frame(root, padding="15 15 15 15")
        self.mainframe.pack(expand=True, fill="both")

        # Label for Summary Page title
        label = ttk.Label(self.mainframe, text="Summary of Recorded Entries", font=("Helvetica", 16))
        label.grid(column=0, row=0, columnspan=3, sticky="w", pady=(5, 15))

        # List all entries in a readable format
        self.entries_list = tk.Listbox(self.mainframe, width=60, height=10, font=("Helvetica", 12))
        self.entries_list.grid(column=0, row=1, columnspan=3, sticky="ew", pady=(10, 10))

        for entry in entries:
            self.entries_list.insert(tk.END, f"Directory: {entry.get('Directory', 'N/A')}, "
                                             f"FileType: {entry['FileType']}, Filename: {entry['FileName']}")

        # Buttons: Back to AddFiles, Encrypt & Save, and Quit
        self.back_button = ttk.Button(self.mainframe, text="Back to Add Files", command=self.back_to_add_files)
        self.back_button.grid(column=0, row=2, pady=(10, 0), sticky="w")

        self.encrypt_button = ttk.Button(self.mainframe, text="Encrypt & Save Entries", command=self.encrypt_and_save)
        self.encrypt_button.grid(column=1, row=2, pady=(10, 0))

        self.quit_button = ttk.Button(self.mainframe, text="Quit", command=root.quit)
        self.quit_button.grid(column=2, row=2, pady=(10, 0), sticky="e")

        # Column and row weights for spacing
        for i in range(3):
            self.mainframe.columnconfigure(i, weight=1)

    def back_to_add_files(self):
        # Go back to the AddFiles page
        self.mainframe.destroy()
        AddFiles(root)

    def encrypt_and_save(self):
        # Encrypt and store entries in binary file
        encrypt_and_store_entries(entries)
        print("Entries encrypted and saved.")
        self.mainframe.destroy()
        WelcomePage(root)

# Main Application
root = tk.Tk()
root.title("HoneyDefense")
root.geometry("600x600")
WelcomePage(root)
root.mainloop()
