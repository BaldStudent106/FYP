import os;
filenames = ["honeyfile1.txt", "honeyfile2.txt", "honeyfile3.txt"]
directory = r"C:\Users\user\Documents"

def createF_files():
    os.makedirs(directory,exist_ok=True)
    for filename in filenames:
        file_path=os.path.join(directory,filename.strip())
        with open(file_path,'w') as honeyfile:
            honeyfile.write("This is a honeyfile");

createF_files()