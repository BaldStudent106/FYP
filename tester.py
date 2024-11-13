import socket

# Replace with the server's IP and port
server_ip = "127.0.0.1"
server_port = 37020

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Send a test message
message = "Test message"
client_socket.sendto(message.encode('utf-8'), (server_ip, server_port))

# Receive response (if any)
client_socket.settimeout(2)  # Wait for a response for 2 seconds
try:
    response, addr = client_socket.recvfrom(4096)
    print(f"Received response from {addr}: {response.decode('utf-8')}")
except socket.timeout:
    print(f"No response from server {server_ip}:{server_port}")

client_socket.close()
