import socket
import thread

class Server():
    BUFFER_SIZE = 4096
    ADDRESS = ("localhost", 8888)
    BACKLOG = 100
    NAME_KEYWORD = "!name!"
    ALL = "all"
    connections = {} # Make a name: connection dictionary
    
    def __init__(self):
        self.s = socket.socket()
        self.s.bind(Server.ADDRESS)
        self.s.listen(Server.BACKLOG)

    def start(self):
        print "Waiting for connections..."
        thread.start_new_thread(self.acceptConnections, (self.s,))
        while True:
            to = raw_input("Enter recipient: ")
            command = raw_input("Enter command: ")
            self.sendCommand(to, command)
            self.s.close()

    def acceptConnections(self, s):
        connectionSocket, addr = s.accept()
        thread.start_new_thread(self.serve, (connectionSocket, addr))

    def serve(self, connectionSocket, addr):
        while True:
            message = connectionSocket.recv(Server.BUFFER_SIZE)
            if Server.NAME_KEYWORD in message:
                name = message.split(Server.NAME_KEYWORD)
                Server.connections[name[1]] = connectionSocket
                print Server.connections
            print message
        
    def sendCommand(self, to, command):
        if to.lower() == Server.ALL:
            for k in Server.connections.keys():
                Server.connections[k].send(command)
        elif to in Server.connections.keys():
            Server.connections[to].send(command)
            
if __name__ == "__main__":
    server = Server()
    server.start()
