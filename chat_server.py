import socket
import threading

HOST = '127.0.0.1'  # Use '0.0.0.0' if connecting from other devices
PORT = 12345
clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            msg = client.recv(1024)
            broadcast(msg)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames.pop(index)
            broadcast(f"{nickname} has left the chat.".encode('utf-8'))
            break

def receive():
    server.listen()
    print(f"🔌 Server listening on {HOST}:{PORT}")
    while True:
        client, addr = server.accept()
        print(f"✅ Connected with {addr}")

        client.send("NICKNAME".encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        broadcast(f"{nickname} joined the chat!".encode('utf-8'))
        client.send("Connected to server.".encode('utf-8'))

# --- Start the server ---
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
receive()
        
