# sys gets the name of operating system
import sys
# os performs the functions on the system
import os
import platform
import socket
import thread

WINDOWS = "win"
ADDRESS = ("localhost", 8888)
BUFFER_SIZE = 4096
OSX = "darwin"
        
s = socket.socket()
s.connect(ADDRESS)
s.send("!name!"+platform.node())
osName = sys.platform
computerName = platform.node()
print computerName
while True:
    received = s.recv(BUFFER_SIZE)
    if osName.startswith(WINDOWS):
        pass
    elif OSX in osName.lower():
        if received == "speak":
            print "About to speak!"
            os.system("say hi")
    else:
        pass
        
        
    
s.close()