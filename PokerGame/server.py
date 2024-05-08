import socket
import threading
from player import player
# Define server address and port
HOST = 'localhost'  # Replace with actual server IP if needed
PORT = 65432

# Define dictionary to store connected clients and their room IDs
connected_clients = {}

def handle_client(conn, addr):
    """Handles communication with a connected client."""
    print(f'Connected by {addr}')
    current_player = None
    try:
        # Check for JOIN message format
        data = conn.recv(1024).decode()
        if data.startswith("JOIN"):
            try:
                room_id = int(data.split()[1])
                name = data.split()[3]
                # Create room if it doesn't exist
                if room_id not in connected_clients:
                    connected_clients[room_id] = []
                    # connected_clients[room_id].append()
                # Add client to the room
                current_player = player(name, conn)
                current_player.room = room_id
                if len(connected_clients[room_id]) == 0:
                    current_player.host = True
                connected_clients[room_id].append(current_player)
                print(f'Client {addr} joined room {room_id}')
                conn.sendall('Joined room successfully!'.encode())
            except (ValueError, IndexError):
                conn.sendall('Invalid room ID format. Please use JOIN <number>'.encode())
                return  # Exit the loop on invalid format
            # ... remaining logic for messages within the room ...
        else:
            conn.sendall('Invalid message format.'.encode())
            return  # Exit the loop on invalid format
        # Broadcast messages to clients in the same room
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            # Print the received message (optional)
            print(f'Client {addr} in room {room_id}: {data}')

            room_clients = connected_clients.get(room_id)
            if(data=="get_number"):
                client.conn.sendall(f'10'.encode())
            if room_clients:
                for client in room_clients:
                    try:
                        # Broadcast message with sender information
                        client.conn.sendall(f'{data}'.encode())
                    except ConnectionAbortedError:
                        print(f'Client {addr} disconnected unexpectedly.')
                        connected_clients[room_id].remove(client)

    except ConnectionError as e:
        print(f'Error communicating with client {addr}: {e}')
    finally:
        if current_player is not None:
            connected_clients[room_id].remove(current_player)
        conn.close()
        print(f'Client {addr} disconnected.')

def main():
    """Starts the server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f'Server listening on {HOST}:{PORT}')

        while True:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()

if __name__ == '__main__':
    main()
