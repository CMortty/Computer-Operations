from networking import Server, WebHandler, AppHandler
import asyncore
import sys
import thread
import platform

HOST, PORT = 'localhost', 8888
OS_NAME = sys.platform
COMPUTER_NAME = platform.node()

class Client(AppHandler):
    def on_msg(self, msg):
        print msg
        
def getText():
    while 1:
        mytxt = raw_input("Text: ")
        client.push(client.encode(mytxt) + '\0')

client = Client(HOST, PORT)
client.push(client.encode("!name!"+COMPUTER_NAME) + '\0')
thread.start_new_thread(getText, ())

asyncore.loop()

