# server.py - Run this first
import socket
import threading
import json
from datetime import datetime

class ChatServer:
    def __init__(self, host='127.0.0.1', port=8051):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.clients = []
        self.usernames = {}
        
    def start(self):
        self.server_socket.listen(2)  # Only allowing 2 connections
        print(f"Server started on {self.host}:{self.port}")
        
        while len(self.clients) < 2:
            client_socket, address = self.server_socket.accept()
            print(f"Connection from {address} established")
            
            client_handler = threading.Thread(
                target=self.handle_client,
                args=(client_socket,)
            )
            client_handler.start()
            
    def handle_client(self, client_socket):
        # Get username
        try:
            username_json = client_socket.recv(1024).decode('utf-8')
            username_data = json.loads(username_json)
            username = username_data.get('username', f"User-{len(self.clients)+1}")
            
            self.clients.append(client_socket)
            self.usernames[client_socket] = username
            
            # Send welcome message
            welcome_msg = {
                "sender": "Server", 
                "message": f"Welcome {username}! There are {len(self.clients)} user(s) connected.",
                "timestamp": datetime.now().strftime("%H:%M:%S")
            }
            client_socket.send(json.dumps(welcome_msg).encode('utf-8'))
            
            # Handle messages
            while True:
                message_json = client_socket.recv(1024).decode('utf-8')
                if not message_json:
                    break
                
                message_data = json.loads(message_json)
                message = message_data.get('message', '')
                
                if message:
                    self.broadcast(message, username)
                    
        except Exception as e:
            print(f"Error: {e}")
        finally:
            # Remove client
            if client_socket in self.clients:
                username = self.usernames.get(client_socket, "Unknown")
                self.clients.remove(client_socket)
                del self.usernames[client_socket]
                self.broadcast(f"{username} has left the chat!", "Server")
                client_socket.close()
    
    def broadcast(self, message, sender):
        msg = {
            "sender": sender, 
            "message": message,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        }
        
        for client in self.clients:
            try:
                client.send(json.dumps(msg).encode('utf-8'))
            except:
                # If can't send message, client is probably disconnected
                if client in self.clients:
                    self.clients.remove(client)
                    if client in self.usernames:
                        del self.usernames[client]

if __name__ == "__main__":
    server = ChatServer()
    server.start()