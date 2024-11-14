import socket
import json

def send_test_message_direct(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        test_message = {
            "device_name": "Test_Client",
            "message": "This is a test message",
            "timestamp": "2024-11-14T10:00:00"
        }
        encrypted_message = json.dumps(test_message).encode('utf-8')  # Modify if encryption is required
        client_socket.sendto(encrypted_message, (ip, port))
        print(f"Test message sent directly to {ip}:{port}")

# Replace with actual server IP and port
send_test_message_direct("192.168.100.136", 37020)  # Example IP and port
