import socket
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QListWidget, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import QTimer

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os



# Server configuration
HOST = '127.0.0.1'
PORT = 54321

lock = threading.Lock()  # Global lock for thread safety


clients = {}  # Maps client names to Client objects
groups = {}   # Maps group names to lists of client names (members)
stored_messages = {}  # Stores messages for inactive clients


server_private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
server_public_key = server_private_key.public_key()



class Client:
    def __init__(self, name, socket, address, session_key):
        self.name = name
        self.socket = socket
        self.address = address
        self.session_key = session_key
        self.status = "Active"

class ChatServer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("csce513fall24Msg Server")
        self.setGeometry(300, 300, 400, 900)
        
        # Main layout
        self.layout = QVBoxLayout()
        
        # Client list display
        self.client_list = QListWidget(self)
        self.layout.addWidget(QLabel("Connected Clients (Active/Inactive):"))
        self.layout.addWidget(self.client_list)
        
        # Group list display
        self.group_list = QTextEdit(self)
        self.group_list.setReadOnly(True)
        self.layout.addWidget(QLabel("Groups and Members:"))
        self.layout.addWidget(self.group_list)
        
        # Chat display area
        self.chat_display = QTextEdit(self)
        self.chat_display.setReadOnly(True)
        self.layout.addWidget(QLabel("Chat Log:"))
        self.layout.addWidget(self.chat_display)
        
        # Set up the central widget and layout
        central_widget = QWidget(self)
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)
        
        # Start the server thread
        threading.Thread(target=self.start_server, daemon=True).start()

    def start_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST, PORT))
        server.listen()
        self.display_message("Server started on port " + str(PORT))
        
        while True:
            client_socket, client_address = server.accept()
            threading.Thread(target=self.handle_client, args=(client_socket, client_address), daemon=True).start()

    def handle_client(self, client_socket, client_address):
      
        server_public_key_bytes = server_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        client_socket.send(server_public_key_bytes)
        
        
        encrypted_session_key = client_socket.recv(256)
        session_key = server_private_key.decrypt(
            encrypted_session_key,
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
        )
        
        
        client_name = client_socket.recv(1024).decode()
        
        with lock:
            if client_name in clients:
                clients[client_name].status = "Active"
                clients[client_name].socket = client_socket
            else:
                clients[client_name] = Client(client_name, client_socket, client_address, session_key)
            
            # Check if there are stored messages for this client and send them
            if client_name in stored_messages:
                self.send_stored_messages(client_name)
                del stored_messages[client_name]  # Clear stored messages after sending
    

        # Schedule client list update in the main thread and broadcast the updated list
        QTimer.singleShot(0, self.update_client_list)
        self.broadcast_client_list()
        self.display_message(f"{client_name} has joined the chat")
        self.broadcast(f"{client_name} has joined the chat", client_name)

        while True:
            try:
                encrypted_message = client_socket.recv(1024)
                if not encrypted_message:
                    break
                data = self.decrypt_message(encrypted_message, session_key).decode()

                with lock:
                    if data.startswith("/create_group"):
                        _, group_name = data.split(" ", 1)
                        self.create_group(client_name, group_name)
                    elif data.startswith("/join_group"):
                        _, group_name = data.split(" ", 1)
                        self.join_group(client_name, group_name)
                    elif data.startswith("/group_msg"):
                        _, group_name, message = data.split(" ", 2)
                        self.group_message(client_name, group_name, message)
                    elif data.startswith("@"):  # Handle direct/private messages
                        target_name, message = data[1:].split(" ", 1)
                        self.private_message(client_name, target_name, message)
                    else:
                        self.broadcast(f"{client_name}: {data}", client_name)
            except:
                break

        with lock:
            clients[client_name].status = "Inactive"
            QTimer.singleShot(0, self.update_client_list)  # Update client list in main thread
            self.broadcast_client_list()
        client_socket.close()
        self.display_message(f"{client_name} has disconnected")
        self.broadcast(f"{client_name} has left the chat", client_name)



    def encrypt_message(self, message, key):
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
        encryptor = cipher.encryptor()
        return iv + encryptor.update(message.encode())
      
      

    def decrypt_message(self, encrypted_message, key):
        iv = encrypted_message[:16]
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
        decryptor = cipher.decryptor()
        return decryptor.update(encrypted_message[16:])


    def send_stored_messages(self, client_name):
        for message in stored_messages[client_name]:
            clients[client_name].socket.send(message.encode())
        self.display_message(f"Delivered stored messages to {client_name}.")

    def store_message(self, recipient_name, message):
        if recipient_name not in stored_messages:
            stored_messages[recipient_name] = []
        stored_messages[recipient_name].append(message)
        self.display_message(f"Stored message for {recipient_name}: {message}")
        
        
        


    def create_group(self, client_name, group_name):
        if group_name in groups:
            clients[client_name].socket.send(f"Group '{group_name}' already exists.".encode())
        else:
            groups[group_name] = [client_name]
            QTimer.singleShot(0, self.update_group_list)  # Update group list in main thread
            self.broadcast_group_list()
            self.display_message(f"Group '{group_name}' created by {client_name}")
            clients[client_name].socket.send(f"Group '{group_name}' created successfully.".encode())

    def join_group(self, client_name, group_name):
        if group_name in groups:
            if client_name not in groups[group_name]:
                groups[group_name].append(client_name)
                QTimer.singleShot(0, self.update_group_list)  # Update group list in main thread
                self.broadcast_group_list()
                self.display_message(f"{client_name} joined group '{group_name}'")
                clients[client_name].socket.send(f"Joined group '{group_name}' successfully.".encode())
            else:
                clients[client_name].socket.send(f"You are already in group '{group_name}'.".encode())
        else:
            clients[client_name].socket.send(f"Group '{group_name}' does not exist.".encode())

    def group_message(self, sender_name, group_name, message):
        if group_name in groups and sender_name in groups[group_name]:
            for member_name in groups[group_name]:
                if clients[member_name].status == "Active":
                    clients[member_name].socket.send(f"[{group_name}] {sender_name}: {message}".encode())
            self.display_message(f"[{group_name}] {sender_name}: {message}")
        else:
            clients[sender_name].socket.send(f"Cannot send message. Group '{group_name}' does not exist or you are not a member.".encode())

    def private_message(self, sender_name, target_name, message):
        if target_name in clients and clients[target_name].status == "Active":
            try:
                clients[target_name].socket.send(f"(Private) {sender_name}: {message}".encode())
                clients[sender_name].socket.send(f"(Private to {target_name}) You: {message}".encode())
                self.display_message(f"(Private) {sender_name} to {target_name}: {message}")
            except socket.error:
                clients[target_name].status = "Inactive"
                QTimer.singleShot(0, self.update_client_list)
                self.broadcast_client_list()
        else:
            self.store_message(target_name, f"(Private) {sender_name}: {message}")
            clients[sender_name].socket.send(f"{target_name} is currently inactive. Message will be delivered when they reconnect.".encode())
            self.display_message(f"{sender_name} tried to message {target_name}, who is inactive. Message stored.")
            



    def broadcast(self, message, sender_name):
        for client_name, client in clients.items():
            if client.status == "Active" and client_name != sender_name:
                try:
                    client.socket.send(message.encode())
                except socket.error:
                    client.status = "Inactive"
                    QTimer.singleShot(0, self.update_client_list)  # Update client list in main thread
        self.display_message(message)

    def broadcast_client_list(self):
        client_names = ",".join(clients.keys())
        for client in clients.values():
            if client.status == "Active":
                client.socket.send(f"CLIENT_LIST_UPDATE:{client_names}".encode())

    def broadcast_group_list(self):
        group_names = ",".join(groups.keys())
        for client in clients.values():
            if client.status == "Active":
                client.socket.send(f"GROUP_LIST_UPDATE:{group_names}".encode())

    def update_client_list(self):
        self.client_list.clear()
        for client_name, client in clients.items():
            self.client_list.addItem(f"{client_name} ({client.status})")

    def update_group_list(self):
        self.group_list.clear()
        for group_name, members in groups.items():
            member_list = ", ".join(members)
            self.group_list.append(f"{group_name}: {member_list}")

    def display_message(self, message):
        self.chat_display.append(message)

if __name__ == "__main__":
    app = QApplication([])
    server = ChatServer()
    server.show()
    app.exec_()