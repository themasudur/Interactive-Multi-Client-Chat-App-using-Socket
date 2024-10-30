## Interactive Multi-client Chat System using Socket in Python

# csce513fall24Msg

`csce513fall24Msg` is a Python-based GUI online chat application designed for students and instructors to communicate in a class setting. This application facilitates real-time, secure, and organized discussions, supporting private and group messages, file transfers, offline messaging, and encrypted communication.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup](#setup)
- [Usage](#usage)
- [Architecture](#architecture)
- [Detailed Explanation of Each Component](#detailed-explanation-of-each-component)
- [Bonus Features](#bonus-features)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Private Messaging**: Direct messaging for one-on-one communication.
- **Group Chat**: Group discussions, with real-time visibility for all members.
- **File Transfer**: Easy file sharing between clients.
- **Offline Messaging**: Stores messages for offline users and delivers them upon reconnection.
- **Secure Communication**: RSA-encrypted message exchange for secure communication.

## Technologies Used

- **Python**: Core programming language.
- **Tkinter**: GUI library for creating cross-platform user interfaces.
- **Socket Programming**: Enables TCP/IP communication for real-time messaging.
- **Multithreading**: Supports multiple concurrent users.
- **Encryption**: Implements RSA for secure message exchanges.

## Setup

### Prerequisites

- Python 3.x
- Basic familiarity with running Python scripts

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/csce513fall24Msg.git
   cd csce513fall24Msg


## Usage

### Client GUI Overview

The client GUI, built with Tkinter, includes the following sections:

- **Login Section**: Allows users to enter their username and connect to the server.
- **Chat Display**: Shows ongoing chat messages and notifications.
- **Message Input**: Users can type messages here. Supports various commands:
  - `@username message`: Direct message to a specific user.
  - `/group group_name message`: Sends message to a specified group.
  - `/file recipient_username path_to_file`: Sends a file to another user.
- **File Transfer**: Supports selecting and sending files.
- **Encryption**: Automatically manages secure communications.

### Example Sessions

- **Starting a Private Chat**:
  - Enter `@username message` in the message input box to chat directly with a user.

- **Group Chat**:
  - Enter `/group group_name message` to send a message to everyone in the specified group.

- **File Transfer**:
  - Use the GUI’s file selection button or input `/file recipient_username path_to_file` to send a file to another client.

## Architecture

The `csce513fall24Msg` system operates on a client-server architecture, where all client communications are routed through the server. The application supports concurrent users, ensuring efficient message handling and enhanced user experience.

- **Server**: Handles all incoming connections, message routing, and user management. Uses multi-threading to support multiple users.
- **Client**: Each client connects to the server and enables real-time chat in a graphical environment. Advanced functionalities like encryption, group chats, and file transfers are seamlessly integrated.
- **Encryption**: RSA-based secure message exchange ensures confidentiality and security.

## Detailed Explanation of Each Component

1. **Server (server.py)**
   - **Socket Initialization**: Creates a TCP/IP socket bound to a specified IP and port.
   - **Connection Management**: Manages client connections and directs messages based on the recipient.
   - **Multi-Threading**: Each client connection is handled by a dedicated thread.
   - **Message Handling**: Routes messages to the intended recipients, supports file transfers, and manages offline message delivery.
   - **Error Handling**: Manages exceptions, such as unexpected client disconnections.

2. **Client (client.py)**
   - **Socket Connection**: Connects to the server using a specific IP and port.
   - **GUI with Tkinter**: The graphical interface includes login, chat display, message input, and file transfer sections.
   - **Commands and Parsing**: Supports commands for direct messaging, group chats, and file transfers.
   - **I/O Multiplexing**: Uses `select` for efficient message sending and receiving without blocking.
   - **Encryption**: Encrypts messages before sending and decrypts upon receipt.

## Bonus Features

### Group Chat

The group chat feature allows multiple users to communicate within a dedicated chat room. Users can join or create a group using `/group group_name`.

### File Transfer

File transfer is initiated through the GUI or by entering `/file recipient_username path_to_file`. Files are sent through the server, ensuring smooth delivery.

### Offline Messaging

If a client is offline, messages sent to them are stored on the server and delivered once they reconnect.

### Secure Communication

RSA encryption is implemented to secure private messages. Each message is encrypted using the recipient's public key and decrypted upon receipt using the recipient's private key.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.



This In this application, we built an online chat system. 

# Problem Statement:

Design and develop an online chat system, named csce513fall24Msg, for communications and discussions among students in a class. The csce513fall24Msg is expected to enable the students to chat with the instructor and their classmates for any necessary discussion, e.g., homework problem. Below are the general guideline for the system design.

1. Client-Server Communication using TCP/IP
The first step is to build a server and a client that can communicate with each other through socket programming using TCP/IP. The communication between two clients will go through the server: if client A wishes to initiate a chat with client B, both A and B should connect to the server and the server should forward messages or requests between A and B. (30 points)

2. Advanced Client
Now you can add the functionality to allow a client to send and receive messages at the same time with less CPU workload. I/O multiplexing can be used in this task. You can use system callback function: a client will be activated if the socket receives data from the server or keyboard input from the user. Hint: try to use select(), poll() and epoll() in your client. (20 points)

3. Multi-Thread Communication Server
We will improve our server in this task to allow multiple students to discuss class topics or homework problems at the same time. You can use any of the following three methods to implement your server: Use socketserver model (Python has provided socketserver package), Thread + socket, I/O multiplexing. Till now, your server should be able to support concurrent connections with multiple clients. (20 points)

4. Client-Client Communication
Now, we are ready to implement the client to client communication in
csce513fall24Msg. Your need to implement three core functions: Client management, Receive message from a sending client, Forward message to a receiving client
Client management is to be implemented in the server, to capture the exception of client absence. For example, if A wishes to chat with B, but B is not in the system, your
server should be robust to handle this issue. Clients communicate with each other by passing messages through the server. In your demo, you should show the client windowfor sender and receiver, and the server window. Necessary information should be displayed on the respective window to demonstrate that your implementation functions well and satisfies the requirement. (30 points)

5. Bonus functionality 
You can get 5 bonus points for the implementation of each extra functionality.
Group chat. Each group member can send and receive messages in the group chat window. These messages are visible to all group members. File transfer. A client can transfer a file to another client by using csce513fall24Msg.
Offline message. The server can save the message for offline clients (not connecting to the server). Once these client get connected to the server, the stored message can be forwarded to them.
Secure communication. To enhance the security of csce513fall24Msg, please come up with a security model and add encryption & decryption in the transmitted messages in this task. Hint: use the public and private key to generate and transmit session key.

6. Submission requirement Please submit: - makefile and readme file to explain how to run your code - screenshot for your demo for each task - technical report to explain your implementation

*Solution*

1. Client-Server Communication using TCP/IP
The first step is to build a server and a client that can communicate with each other through socket programming using TCP/IP. The communication between two clients will go through the server: if client A wishes to initiate a chat with client B, both A and B should connect to the server and the server should forward messages or requests between A and B. (30 points)
Steps to implement the server: 
Create a socket for communication
Bind the local port and connection address 
Configure TCP protocol with port number 
Listen for client connection 
Accept connection from client 
Send Acknowledgment 
Receive message from client 
Send message to client

Steps to implement the client: 
Create a socket for communication
Configure TCP protocol with IP address of server and port number 
Connect with server through socket Wait for acknowledgement from server 
Send message to server 
Receive message from server

Using command line is fine, while GUI is highly encouraged. Any language is
acceptable. Python and Java are recommended as they offer convenient tools for socket
programming.

2. Advanced Client
Now you can add the functionality to allow a client to send and receive messages at the
same time with less CPU workload. I/O multiplexing can be used in this task. You can
use system callback function: a client will be activated if the socket receives data from
the server or keyboard input from the user. Hint: try to use select(), poll() and epoll() in
your client. (20 points)

3. Multi-Thread Communication Server
We will improve our server in this task to allow multiple students to discuss class
topics or homework problems at the same time. You can use any of the following three
methods to implement your server:
Use socketserver model (Python has provided socketserver package)
Thread + socket
I/O multiplexing
Till now, your server should be able to support concurrent connections with multiple
clients. (20 points)

4. Client-Client Communication
Now, we are ready to implement the client to client communication in
csce513fall24Msg. Your need to implement three core functions:
Client management
Receive message from a sending client
Forward message to a receiving client
Client management is to be implemented in the server, to capture the exception of
client absence. For example, if A wishes to chat with B, but B is not in the system, your
server should be robust to handle this issue. Clients communicate with each other by
passing messages through the server. In your demo, you should show the client windowfor sender and receiver, and the server window. Necessary information should be displayed on the respective window to demonstrate that your implementation functions well and satisfies the requirement. (30 points)

5. Bonus functionality You can get 5 bonus points for the implementation of each extra functionality.
Group chat. Each group member can send and receive messages in the group chat window. These messages are visible to all group members. File transfer. A client can transfer a file to another client by using csce513fall24Msg.
Offline message. The server can save the message for offline clients (not connecting to the server). Once these client get connected to the server, the stored message can be forwarded to them.
Secure communication. To enhance the security of csce513fall24Msg, please come up with a security model and add encryption & decryption in the transmitted messages in this task. Hint: use the public and private key to generate and transmit session key.

> $ git clone https://github.com/Rishija/python_chatServer.git

## About 
This is a simple multi-client chat server using `sockets` written in `python`. 

The server asks for username when user wants to join the chatroom and accepts the connection only if the username is unique. It then broadcasts the message from one client to all other clients connected. Also informs about the entry/exit of any client.

## Download
Run the following command in your terminal to save the repository in your system
> $ git clone https://github.com/Rishija/python_chatServer.git

## Run
Once you are in the directory where `server.py` or `client.py` file exists, run by typing the following commands in your terminal.

### Server
> $ python server.py

### Client
> $ python client.py hostname

#### Example
For server and client running on the same system

**Server**
> $ python server.py
<pre>
				SERVER WORKING 
Client (127.0.0.1, 51638) connected  [ tesla ]
Client (127.0.0.1, 51641) connected  [ albert ]
Client (127.0.0.1, 51641) is offline  [ albert ]
</pre>



**Client 1**
> $ python client.py localhost

<pre>
CREATING NEW ID:
Enter username: tesla
Welcome to chat room. Enter 'tata' anytime to exit
You: Hello
albert joined the conversation 
albert: world
albert left the conversation
You:
</pre>

**Client 2**
> $ python client.py localhost
<pre>
CREATING NEW ID:
Enter username: albert
Welcome to chat room. Enter 'tata' anytime to exit
You: World
You: tata
DISCONNECTED!!
</pre>
