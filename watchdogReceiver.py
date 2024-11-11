import socket
import json
from encryptionhandler import asymmetric_encryption

# Load the private key for decryption
base_dir = os.path.abspath(os.path.dirname(__file__))
private_key_path = os.path.join(base_dir, 'private_key.pem')
with open(private_key_path, 'rb') as f:
    priv_key = asymmetric_encryption.load_key(f.read(), key_type="private")

def start_receiving_host():
    # Listen for broadcast discovery requests from sending hosts
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind(('', 37020))  # Bind to the broadcast port
        print("Receiving host listening for broadcast discovery requests on port 37020.")

        while True:
            data, addr = sock.recvfrom(1024)  # Receive broadcast
            try:
                message = json.loads(data.decode('utf-8'))
                if message.get("message") == "Request for receiving host":
                    print(f"Received broadcast request from {addr}")
                    
                    # Respond to the sender to confirm that this host is available
                    response_message = json.dumps({"response": "Host available"}).encode('utf-8')
                    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as response_sock:
                        response_sock.sendto(response_message, (addr[0], 37021))
                    print(f"Sent response to {addr[0]} confirming availability.")

            except json.JSONDecodeError:
                print("Received an invalid message.")

            # Once connected, listen for log data
            data, addr = sock.recvfrom(4096)
            decrypted_message = asymmetric_encryption.decrypt_message(data, priv_key)
            log_info = json.loads(decrypted_message)
            print(f"Received log info from {addr}: {log_info}")

# Start the receiving host
start_receiving_host()
