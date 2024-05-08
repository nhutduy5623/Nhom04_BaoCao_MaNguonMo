import socket


def send_tcp_request(host, port, message):
    """Send a TCP request to the server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            port = int(port)  # Convert port to integer
        except ValueError:
            print("Error: Invalid port number")
            return None

        try:
            s.connect((host, port))
            s.sendall(message.encode())
            response = s.recv(1024)  # Adjust buffer size according to your needs
            return response.decode()
        except Exception as e:
            print(f"Error: {e}")
            return None


# Example usage:
NGROK_HOST = '0.tcp.ap.ngrok.io'  # Replace with your Ngrok forwarding host
NGROK_PORT = '12542'  # Replace with your Ngrok forwarding port
MESSAGE = "get_playerMoney"

response = send_tcp_request(NGROK_HOST, NGROK_PORT, MESSAGE)
if response:
    print("Server response:", response)
else:
    print("Failed to send request to the server.")
