import os
import json
import socket
from cryptidy import asymmetric_encryption  # Assuming cryptidy handles encryption/decryption
import time
from zeroconf import ServiceInfo, Zeroconf
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

def get_local_ip():
    """Returns the local IP address of the server."""
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print(f"Local IP for mDNS registration: {local_ip}")
    return local_ip

def load_private_key():
    """Load the private key for decryption (you must implement this)."""
    pass

def save_log(device_name, log_info):
    """Logic to save or process the log information."""
    pass

def start_mdns_server():
    """Starts the mDNS server, registers the service, and listens for UDP messages."""
    private_key = load_private_key()
    zeroconf = Zeroconf()
    service_type = "_logserver._udp.local."
    service_name = "LogServer._logserver._udp.local."
    service_port = 37020

    # Get the local IP address of the server
    local_ip = get_local_ip()

    # Register the service with mDNS using the actual IP address
    service_info = ServiceInfo(
        service_type,
        service_name,
        addresses=[socket.inet_aton(local_ip)],
        port=service_port,
        properties={"message": "Host available"},
        server="LogServer.local.",
    )

    zeroconf.register_service(service_info)
    print(f"mDNS Service registered as LogServer on {local_ip}:{service_port}")

    # Set up UDP socket to listen for incoming messages on the local IP
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((local_ip, service_port))
        print(f"Server listening for encrypted log messages on {local_ip}:{service_port}...")

        try:
            while True:
                # Receive encrypted log messages
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

        except Exception as e:
            print(f"Error occurred: {e}")

        finally:
            # Unregister mDNS service and close Zeroconf
            zeroconf.unregister_service(service_info)
            zeroconf.close()
            print("mDNS Service unregistered.")

# Start the mDNS server
start_mdns_server()