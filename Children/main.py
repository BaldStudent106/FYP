import argparse
from gui import *
import honeyfilesGenerator
import watchdogHandler
from encryptionhandler import *

def run_gui():
    try:
        mainloop_starter()
        honeyfilesGenerator.createF_files()
        watchdogHandler.monitor_directories_and_files()
    except Exception as e:
        print(f"Error in run_gui: {e}")

def run_startup():
    try:
        watchdogHandler.monitor_directories_and_files(decrypt_and_load_entries())
    except Exception as e:
        print(f"Error in run_startup: {e}")

def main():
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description="A program with different functions based on command-line arguments.")

    # Add arguments for different modes; make 'mode' optional with nargs='?' and default to 'gui'
    parser.add_argument("mode", choices=["startup", "gui"], nargs='?', default="gui",
                        help="Mode to run the program in ('gui' or 'startup')")

    # Parse the arguments
    args = parser.parse_args()

    # Run the appropriate function based on the argument
    if args.mode == "startup":
        run_startup()
    else:
        run_gui()

if __name__ == "__main__":
    main()
