import os;
from encryptionhandler import *

def createF_files(entries=decrypt_and_load_entries()):
    for entry in entries:
        # Retrieve directory, filename, and file type from each entry
        directory = entry.get('Directory')
        filename = entry.get('FileName')
        file_type = entry.get('FileType')
        
        # Ensure the directory exists, create if not
        os.makedirs(directory, exist_ok=True)
        
        # Define the complete file path
        file_path = os.path.join(directory, filename.strip())
        
        # Determine the content based on file type
        if file_type == "Text File":
            content = "This is a honeyfile of type Text File."
        elif file_type == "PDF":
            content = "This is a honeyfile of type PDF (placeholder text)."
        elif file_type == "Image":
            content = "This is a placeholder for an image file."
        elif file_type == "Video":
            content = "This is a placeholder for a video file."
        else:
            content = "This is a generic honeyfile."
        
        # Create and write to the file
        with open(file_path, 'w') as honeyfile:
            honeyfile.write(content)

        print(f"Created {file_type} at: {file_path}")


createF_files()