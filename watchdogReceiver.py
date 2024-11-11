import os
import json
import socket
from cryptidy import asymmetric_encryption  # Assuming cryptidy handles encryption/decryption
import time

# Path to store logs
LOG_DIRECTORY = "received_logs"
PRIVATE_KEY_PATH = "private_key.pem"  # Path to private key file

# Load the private key for decryption
def load_private_key():
    with open(PRIVATE_KEY_PATH, "r") as key_file:
        return asymmetric_encryption.load_private_key(key_file.read())

# Organize and save the logs based on device name and timestamp
def save_log(device_name, log_info):
    # Create a directory for the device if it doesn't exist
    device_dir = os.path.join(LOG_DIRECTORY, device_name)
    os.makedirs(device_dir, exist_ok=True)
    
    # Use timestamp as filename to avoid overwriting
    timestamp = log_info.get("timestamp", time.time())
    filename = f"log_{int(timestamp)}.json"
    file_path = os.path.join(device_dir, filename)
    
    # Save the log information in JSON format
    with open(file_path, "w") as log_file:
        json.dump(log_info, log_file, indent=4)
    print(f"Log saved for device '{device_name}' at {file_path}")

def start_udp_server():
    private_key = load_private_key()

    # Set up UDP socket to listen for messages
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind(('', 37020))  # Bind to port 37020

        print("Server listening for logs on port 37020...")

        while True:
            try:
                # Receive encrypted message
                encrypted_message, addr = server_socket.recvfrom(4096)
                print(f"Received message from {addr}")

                # Decrypt the message
                log_info_json = asymmetric_encryption.decrypt_message(encrypted_message, private_key)
                log_info = json.loads(log_info_json)

                # Extract device name and save log
                device_name = log_info.get("device_name", "Unknown_Device")
                save_log(device_name, log_info)
            
            except Exception as e:
                print(f"Error receiving or processing message: {e}")

if __name__ == "__main__":
    start_udp_server()
