import socket
import threading
from datetime import datetime

def log_attempt(ip, port):
    """Logs connection attempts with timestamp."""
    with open("rdp_honeypot_log.txt", "a") as log_file:
        log_file.write(f"[{datetime.now()}] Connection attempt from {ip}:{port}\n")
    print(f"Logged attempt from {ip}:{port}")

def handle_connection(conn, addr):
    """Handles incoming connection to the RDP honeypot."""
    print(f"Connection attempt from {addr[0]}:{addr[1]}")
    log_attempt(addr[0], addr[1])
    
    # Simulate an RDP response (handshake failure or protocol error)
    conn.send(b"\x03\x00\x00\x13\x0e\xd0\x00\x00\x12\x34\x00\x02\x00\x08\x00\x03\x00\x00")
    conn.close()

def start_honeypot(port=3389):
    """Starts the RDP honeypot."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", port))
    server.listen(5)
    print(f"RDP honeypot listening on port {port}...")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_connection, args=(conn, addr)).start()

if __name__ == "__main__":
    start_honeypot()
