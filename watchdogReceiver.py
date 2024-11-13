import os
import json
import socket
from cryptidy import asymmetric_encryption  # Assuming cryptidy handles encryption/decryption
import time
from Cryptodome.PublicKey import RSA

# Path to store logs
LOG_DIRECTORY = "received_logs"
PRIVATE_KEY_PATH = "private_key.pem"  # Path to private key file

# Load the private key for decryption
def load_private_key():
    with open(PRIVATE_KEY_PATH, "rb") as key_file:
        return RSA.import_key(key_file.read())  # Corrected: Use RSA.import_key to load the private key

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

    # Set up UDP socket to listen for incoming messages on port 37020
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        server_socket.bind(('0.0.0.0', 37020))  # Bind to port 37020 for log messages
        print("Server listening on port 37020...")

        while True:
            try:
                # Receive a discovery request (from the send_log_info function)
                discovery_message, addr = server_socket.recvfrom(4096)
                print(f"Received discovery request from {addr}")

                # Decode the discovery request message
                discovery_data = json.loads(discovery_message.decode('utf-8'))

                if discovery_data.get("message") == "Request for receiving host":
                    print(f"Discovery request received from {addr}, responding with host availability.")

                    # Respond with "Host available" message
                    response_data = {"response": "Host available"}
                    response_message = json.dumps(response_data).encode('utf-8')

                    # Send the response back to the sender (the client who discovered the host)
                    server_socket.sendto(response_message, addr)

                # Now listen for an encrypted log message
                encrypted_message, addr = server_socket.recvfrom(4096)
                print(f"Received encrypted log message from {addr}")

                # Decrypt the message using the private key
                log_info_json = asymmetric_encryption.decrypt_message(encrypted_message, private_key)

                # Parse the decrypted JSON message
                log_info = json.loads(log_info_json)

                # Extract the device name and save the log
                device_name = log_info.get("device_name", "Unknown_Device")
                print(f"Device: {device_name}, Message: {log_info['message']}, Timestamp: {log_info['timestamp']}")
                
                save_log(device_name, log_info)

            except:
                pass

start_udp_server()
