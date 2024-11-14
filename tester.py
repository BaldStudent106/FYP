import socket
import json
from zeroconf import ServiceBrowser, Zeroconf

class LogServerListener:
    def __init__(self):
        self.server_address = None

    def add_service(self, zeroconf, service_type, name):
        """Callback method when a new service is discovered."""
        info = zeroconf.get_service_info(service_type, name)
        if info:
            server_ip = socket.inet_ntoa(info.addresses[0])
            server_port = info.port
            self.server_address = (server_ip, server_port)
            print(f"Discovered LogServer at {server_ip}:{server_port}")

    def update_service(self, zeroconf, service_type, name):
        """Required update_service method, can be empty if updates are not needed."""
        pass

    def get_server_address(self):
        return self.server_address

def send_test_message():
    """Sends a test message to the discovered server."""
    zeroconf = Zeroconf()
    listener = LogServerListener()

    # Browse for the LogServer service on mDNS
    ServiceBrowser(zeroconf, "_logserver._udp.local.", listener)
    
    try:
        # Wait for service discovery to complete
        import time
        time.sleep(2)  # Adjust this time if necessary for discovery

        # Get the server address discovered via mDNS
        server_address = listener.get_server_address()
        if server_address is None:
            print("LogServer service not found.")
            return
        
        # Create a UDP socket to send a test message
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
            test_message = {"device_name": "Test_Client", "message": "This is a test message", "timestamp": "2024-11-14T10:00:00"}
            encrypted_message = json.dumps(test_message).encode('utf-8')  # Modify if encryption is required

            # Send the test message to the server
            client_socket.sendto(encrypted_message, server_address)
            print(f"Test message sent to {server_address}")
    
    finally:
        zeroconf.close()

# Run the test message function
send_test_message()
