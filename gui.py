import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

class WelcomePage:
    def __init__(self, root):
        # Frame and widgets for Welcome Page
        self.mainframe = ttk.Frame(root, padding="3 3 12 12")
        label = ttk.Label(self.mainframe, text="Welcome to HoneyDefense")
        button = ttk.Button(self.mainframe, text="Next Page", command=self.next_page)
        separator = ttk.Separator(self.mainframe, orient="horizontal")
        
        # Layout configuration
        self.mainframe.pack(expand=True, fill="both")
        label.grid(column=1, row=0)
        separator.grid(column=0, row=1, columnspan=4, sticky="ew")
        button.grid(column=3, row=3)

        # Column and row weights
        for i in range(3):
            self.mainframe.columnconfigure(i, weight=1)
            self.mainframe.rowconfigure(i, weight=1)

    def next_page(self):
        self.mainframe.destroy()
        AddFiles(root)

entries=[]
tempentries={}

class AddFiles:
    def __init__(self, root):
        # List to store entries from the AddFiles page (shared across instances)
        self.entries = []
        self.tempentries ={}

        # Frame for AddFiles page
        self.mainframe = ttk.Frame(root, padding="3 3 12 12")
        self.mainframe.pack(expand=True, fill="both")

        # Label for the Add Files page title
        label = ttk.Label(self.mainframe, text="Welcome to Add Files Page")
        label.grid(column=0, row=0, columnspan=2, sticky="w")

        # Button to select directory
        self.select_dir_button = ttk.Button(self.mainframe, text="Select Directory", command=self.askfiledirectory)
        self.select_dir_button.grid(column=0, row=1, pady=(10, 5), sticky="w")

        # Listbox for file type selection
        self.file_type_label = ttk.Label(self.mainframe, text="Select File Type:")
        self.file_type_label.grid(column=0, row=2, sticky="w")

        self.file_type_listbox = tk.Listbox(self.mainframe, height=4, selectmode="single", exportselection=False)
        self.file_type_listbox.insert(1, "Text File")
        self.file_type_listbox.insert(2, "PDF")
        self.file_type_listbox.insert(3, "Image")
        self.file_type_listbox.insert(4, "Video")
        self.file_type_listbox.grid(column=1, row=2, sticky="ew")

        # Entry for filename
        self.filename_label = ttk.Label(self.mainframe, text="Enter Filename:")
        self.filename_label.grid(column=0, row=3, sticky="w")

        self.filename_entry = ttk.Entry(self.mainframe, width=20)
        self.filename_entry.grid(column=1, row=3, sticky="ew")

        # Back, Add Another File, and Next buttons
        self.back_button = ttk.Button(self.mainframe, text="Back", command=self.go_back)
        self.back_button.grid(column=0, row=4, pady=(10, 0), sticky="w")

        self.add_another_button = ttk.Button(self.mainframe, text="Add Another File", command=self.add_another_file)
        self.add_another_button.grid(column=1, row=4, pady=(10, 0))

        self.next_button = ttk.Button(self.mainframe, text="Next", command=self.save_and_next)
        self.next_button.grid(column=1, row=5, pady=(10, 0), sticky="e")

        # Column and row weights
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.columnconfigure(1, weight=2)
        self.mainframe.rowconfigure(5, weight=1)

    def askfiledirectory(self):
        # Function to ask for directory
        directory = filedialog.askdirectory()
        if directory:
            print("Selected directory:", directory)
            tempentries["Directory"]=directory  # Save directory to entries list

    def go_back(self):
        # Return to the WelcomePage
        self.mainframe.destroy()
        WelcomePage(root)

    def add_another_file(self):
        # Save the current entry and reset fields for another file entry
        file_type = self.file_type_listbox.get(tk.ACTIVE)
        filename = self.filename_entry.get()
        
        if file_type and filename:
            # Add current entry to entries list
            tempentries['FileType'] =file_type
            tempentries['FileName'] = filename
            entries.append(tempentries.copy())
            tempentries.clear()
            print("Added entry:", entries[-1])  # Print latest entry for verification
        
        # Clear fields for next entry
        self.filename_entry.delete(0, tk.END)
        self.file_type_listbox.selection_clear(0, tk.END)

    def save_and_next(self):
        # Save current entry, then navigate to SummaryPage
        self.add_another_file()  # Save current entry if any fields are filled
        print("Entries:", self.entries)  # Print all entries
        
        self.mainframe.destroy()
        SummaryPage(root)

class SummaryPage:
    def __init__(self, root):
        # Frame for SummaryPage
        self.mainframe = ttk.Frame(root, padding="3 3 12 12")
        self.mainframe.pack(expand=True, fill="both")

        # Label for Summary Page title
        label = ttk.Label(self.mainframe, text="Summary of Recorded Entries")
        label.grid(column=0, row=0, columnspan=2, sticky="w")

        # List all entries in a readable format
        self.entries_list = tk.Listbox(self.mainframe, width=50, height=10)
        self.entries_list.grid(column=0, row=1, columnspan=2, sticky="ew")
        
        for entry in entries:
            self.entries_list.insert(tk.END, f"Directory: {entry.get('Directory', 'N/A')}, "
                                             f"FileType: {entry['FileType']}, Filename: {entry['FileName']}")

        # Back button to return to AddFiles page
        self.back_button = ttk.Button(self.mainframe, text="Back to Add Files", command=self.back_to_add_files)
        self.back_button.grid(column=0, row=2, pady=(10, 0), sticky="w")

        # Quit button to exit
        self.quit_button = ttk.Button(self.mainframe, text="Quit", command=root.quit)
        self.quit_button.grid(column=1, row=2, pady=(10, 0), sticky="e")

    def back_to_add_files(self):
        # Go back to AddFiles with current entries
        self.mainframe.destroy()
        AddFiles(root)

# Root window setup
root = tk.Tk()
app = WelcomePage(root)
root.mainloop()
