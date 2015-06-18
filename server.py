import socket
import thread

BUFFER_SIZE = 4096
ADDRESS = ("localhost", 8888)
BACKLOG = 100
NAME_KEYWORD = "!name!"
connections = {} # Make a name: connection dictionary

def serve(connectionSocket, addr):
    while True:
        message = connectionSocket.recv(BUFFER_SIZE)
        if (NAME_KEYWORD in message):
            name = message.split(NAME_KEYWORD)
            connections[name[1]] = connectionSocket
            print connections
        print message

s = socket.socket()
s.bind(ADDRESS)
s.listen(BACKLOG)
print "Waiting for connections..."
while True:
    connectionSocket, addr = s.accept()
    thread.start_new_thread( serve, (connectionSocket, addr))
s.close()
