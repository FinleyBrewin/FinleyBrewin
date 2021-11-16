# importing needed libraries
import threading
import socket

# print to let user know the program has launched
print("Server launched...")

# creating variables for use later
HOSTIP = "0.0.0.0" # IP for the server connection, in this case localhost IP
PORT = 22222 # port for the server connection
FORMAT = "ascii" # format to send messages in
clients = []
names = []

# creating sockets for the server to host
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # setting up the socket
server.bind((HOSTIP, PORT)) # binding the socket with the server IP and Port
server.listen(5) # listening to see if any clients are connecting (will queue up to 5 connections)
# letting the user know what IP and port the server is hosting on
print(f"Listening as {HOSTIP}:{PORT}")


# Function to send messages to all connected sockets
def send(message):
    for client in clients:
        client.send(message)


# Function to handle all the messages sent from the other clients and send them to everyone else
def handle(client):
    while True:
        try:
            # tries to receive a message from client
            message = client.recv(1024)
            send(message)
        except:
            # If the server doesnt receive a message from a client it kicks it from the server
            name = clients.index(client)
            clients.remove(client)
            client.close()
            name = names[name]
            names.remove(name)
            send(f"{name} disconnected!".encode(FORMAT)) # sends a message to all connected clients that this client has disconnected
            print(f"{name} disconnected!") # sends to server client
            #also sends updated name list to clients
            namelist = ' '.join(names)
            send(f"{'ufs712464'} {namelist}".encode(FORMAT))
            break


# main function to accept the clients and add them to client and names list and manage messages
def main():
    while True:
        client, address = server.accept()
        print(f"{address}" " has connected")
        #sends "Name" to the connected user to recieve the name they picked
        client.send("Name".encode(FORMAT))
        name = client.recv(1024).decode(FORMAT)
        # when a client connects it adds the client and name to the lists
        names.append(name)
        clients.append(client)
        # sends list of other names
        namelist = ' '.join(names)
        send(f"{'ufs712464'} {namelist}".encode(FORMAT))

        # tells server and other clients when a user joins
        print("The user set their name as " + name)
        send(f"{name} connected!".encode(FORMAT))
        client.send(" welcome".encode(FORMAT))

        # allocates a thread to individual client requests
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Waiting for clients...")
main() # starting main function loop