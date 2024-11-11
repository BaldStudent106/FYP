import PyInstaller.__main__
import subprocess
import os
import tkinter as tk
from tkinter import ttk, filedialog
from cryptidy import asymmetric_encryption
import json

class WelcomePage:
    def __init__(self, root):
        self.mainframe = ttk.Frame(root, padding="15 15 15 15")
        label = ttk.Label(self.mainframe, text="Welcome to HoneyDefense", font=("Helvetica", 16))
        button = ttk.Button(self.mainframe, text="Next Page", command=self.next_page)
        separator = ttk.Separator(self.mainframe, orient="horizontal")
        
        self.mainframe.pack(expand=True, fill="both")
        label.grid(column=1, row=0, pady=(10, 10))
        separator.grid(column=0, row=1, columnspan=4, sticky="ew", pady=(10, 10))
        button.grid(column=3, row=3, padx=(10, 10), pady=(10, 10))
        
        for i in range(4):
            self.mainframe.columnconfigure(i, weight=1)
            self.mainframe.rowconfigure(i, weight=1)

    def next_page(self):
        self.mainframe.destroy()
        AddFiles(root)


class AddFiles:
    def __init__(self, root):
        self.mainframe = ttk.Frame(root, padding="15 15 15 15")
        label = ttk.Label(self.mainframe, text="Please download Inno Setup to proceed.", font=("Helvetica", 14))
        label.grid(column=1, row=0, pady=(10, 10))
        
        link = ttk.Label(self.mainframe, text="Download Inno Setup", font=("Helvetica", 12), foreground="blue", cursor="hand2")
        link.grid(column=1, row=1, pady=(10, 10))
        link.bind("<Button-1>", lambda e: self.open_download_link())
        
        next_button = ttk.Button(self.mainframe, text="Next", command=self.next_page)
        next_button.grid(column=1, row=2, pady=(10, 10))
        
        self.mainframe.pack(expand=True, fill="both")
        
        for i in range(3):
            self.mainframe.columnconfigure(i, weight=1)
            self.mainframe.rowconfigure(i, weight=1)
    
    def open_download_link(self):
        import webbrowser
        webbrowser.open("https://jrsoftware.org/isdl.php")

    def next_page(self):
        self.mainframe.destroy()
        ChooseInstallLocationPage(root)


class ChooseInstallLocationPage:
    def __init__(self, root):
        self.mainframe = ttk.Frame(root, padding="15 15 15 15")
        label = ttk.Label(self.mainframe, text="Choose Installation Directory", font=("Helvetica", 14))
        label.grid(column=1, row=0, pady=(10, 10))
        
        self.default_path = os.path.join(os.environ.get('ProgramFiles', 'C:\\Program Files'), "WatchdogHandler")
        
        self.install_path_var = tk.StringVar(value=self.default_path)
        install_path_label = ttk.Label(self.mainframe, text="Installation Directory:")
        install_path_label.grid(column=1, row=1, sticky="w", padx=(10, 0))
        self.install_path_entry = ttk.Entry(self.mainframe, textvariable=self.install_path_var, width=50)
        self.install_path_entry.grid(column=1, row=2, padx=(10, 10), pady=(5, 10))

        browse_button = ttk.Button(self.mainframe, text="Browse...", command=self.select_directory)
        browse_button.grid(column=2, row=2, padx=(5, 10))
        
        continue_button = ttk.Button(self.mainframe, text="Continue", command=self.proceed_with_install)
        continue_button.grid(column=1, row=3, pady=(15, 10))
        
        self.mainframe.pack(expand=True, fill="both")
        
        for i in range(3):
            self.mainframe.columnconfigure(i, weight=1)
            self.mainframe.rowconfigure(i, weight=1)

    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.install_path_var.set(directory)

    def proceed_with_install(self):
        install_path = self.install_path_var.get()
        print(f"Selected installation path: {install_path}")
        self.mainframe.destroy()
        GenerateExePage(root, install_path)


class GenerateExePage:
    def __init__(self, root, install_path):
        self.install_path = install_path
        self.mainframe = ttk.Frame(root, padding="15 15 15 15")
        
        label = ttk.Label(self.mainframe, text="Click to generate an encrypted executable", font=("Helvetica", 14))
        label.grid(column=1, row=0, pady=(10, 10))
        
        generate_button = ttk.Button(self.mainframe, text="Generate Encrypted Exe", command=self.generate_exe)
        generate_button.grid(column=1, row=1, pady=(10, 10))
        
        self.mainframe.pack(expand=True, fill="both")
        
        for i in range(3):
            self.mainframe.columnconfigure(i, weight=1)
            self.mainframe.rowconfigure(i, weight=1)

    def generate_exe(self):
        base_dir = os.path.abspath(os.path.dirname(__file__))

        # Define paths relative to the base directory
        source_script = os.path.join(base_dir, 'watchdogHandler.py')
        dist_path = os.path.join(base_dir, 'dist')
        build_path = os.path.join(base_dir, 'build')
        spec_path = os.path.join(base_dir, 'spec')
        output_dir = os.path.join(base_dir, 'output')
        inno_script_path = os.path.join(base_dir, 'installer_script.iss')
        private_key_path = os.path.join(base_dir, 'private_key.pem')
        public_key = None  # Initialize public_key to None 

        if os.path.exists(private_key_path):
            with open(private_key_path, 'rb') as f:
                priv_key = asymmetric_encryption.load_key(f.read(), key_type="private")
            pub_key = priv_key.public_key()
            print("Loaded existing keys.")
        else:
            priv_key, pub_key = asymmetric_encryption.generate_keys(2048)
            with open(private_key_path, 'wb') as f:
                f.write(priv_key.save_key())
            print("Generated and stored new key pair.")

        public_key_str = pub_key.save_key().decode("utf-8").replace("\n", "\\n")

        setup_script = f"""
        [Setup]
        AppName=WatchdogHandler
        AppVersion=1.0
        DefaultDirName={self.install_path}
        DefaultGroupName=WatchdogHandler
        OutputDir={output_dir}
        OutputBaseFilename=WatchdogHandlerInstaller
        Compression=lzma
        SolidCompression=yes

        [Files]
        Source: "{dist_path}\\watchdogHandler.exe"; DestDir: "{{app}}"; Flags: ignoreversion

        [Icons]
        Name: "{{group}}\\WatchdogHandler"; Filename: "{{app}}\\watchdogHandler.exe"

        [INI]
        Filename: "{{app}}\\config.ini"; Section: "Security"; Key: "PublicKey"; String: "{public_key_str}"
        """
        
        with open(inno_script_path, "w") as f:
            f.write(setup_script)
        
        if os.path.exists(inno_setup_path):
            subprocess.call([inno_setup_path, inno_script_path])
            print("Installer creation complete.")
        else:
            print("Inno Setup compiler not found. Please ensure Inno Setup is installed and the path is correct.")

        sample_data = ["foo", "bar", "some long string", 12]
        encrypted = asymmetric_encryption.encrypt_message(sample_data, pub_key)
        decrypted_data = asymmetric_encryption.decrypt_message(encrypted, priv_key)

        print("Data encrypted and decrypted successfully:", decrypted_data)


root = tk.Tk()
root.title("HoneyDefense")
WelcomePage(root)
root.mainloop()
