import configparser
import time
import socket
import json
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from encryptionhandler import asymmetric_encryption  # Assuming this handles encryption/decryption

# Load the public key from the generated config file
def load_public_key_from_ini():
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), "config.ini"))
    
    try:
        public_key_str = config["Security"]["PublicKey"]
        return asymmetric_encryption.load_public_key(public_key_str)
    except KeyError as e:
        print("Error reading public key from config file:", e)
        return None

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, pub_key, receiver_ip=None):
        self.pub_key = pub_key
        self.receiver_ip = receiver_ip

    def on_modified(self, event):
        if event.is_directory:
            return
        print(f"File modified: {event.src_path}")
        self.send_log_info(event.src_path)

    def on_created(self, event):
        if event.is_directory:
            return
        print(f"File created: {event.src_path}")
        self.send_log_info(event.src_path)

    def on_deleted(self, event):
        if event.is_directory:
            return
        print(f"File deleted: {event.src_path}")

    def on_moved(self, event):
        print(f"File moved: {event.src_path} -> {event.dest_path}")

    def send_log_info(self, file_path):
        log_info = {
            "message": "Log update",
            "file_path": file_path,
            "timestamp": time.time()
        }
        log_info_json = json.dumps(log_info)
        encrypted_message = asymmetric_encryption.encrypt_message(log_info_json, self.pub_key)

        if self.receiver_ip:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.sendto(encrypted_message, (self.receiver_ip, 37020))
            print(f"Sent log info to {self.receiver_ip}")
        else:
            print("No receiver host found. Broadcasting to find receiver.")
            self.find_receiver_host(encrypted_message)

    def find_receiver_host(self, encrypted_message):
        # Broadcast to find receiver
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            discovery_message = json.dumps({"message": "Request for receiving host"}).encode('utf-8')
            sock.sendto(discovery_message, ("<broadcast>", 37020))

        # Listen for receiver response
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.bind(('', 37021))
            sock.settimeout(5)
            try:
                response, addr = sock.recvfrom(1024)
                response_data = json.loads(response.decode('utf-8'))
                if response_data.get("response") == "Host available":
                    self.receiver_ip = addr[0]
                    print(f"Found receiver host at {self.receiver_ip}")
                    # Send the previously encrypted message to the newly found host
                    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                        sock.sendto(encrypted_message, (self.receiver_ip, 37020))
            except socket.timeout:
                print("No receiving host responded to the broadcast.")

def monitor_directory_and_file(directory, filename):
    pub_key = load_public_key_from_ini()  # Load the public key from config.ini
    
    if not pub_key:
        print("Public key could not be loaded. Exiting.")
        return

    if not os.path.isdir(directory):
        print(f"Directory {directory} does not exist.")
        return
    
    file_to_watch = os.path.join(directory, filename)
    
    if not os.path.exists(file_to_watch):
        print(f"The file {file_to_watch} does not exist.")
        return

    event_handler = FileChangeHandler(pub_key)
    observer = Observer()
    
    observer.schedule(event_handler, directory, recursive=False)
    observer.schedule(event_handler, file_to_watch, recursive=False)
    
    print(f"Monitoring directory: {directory} and file: {file_to_watch}")

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()