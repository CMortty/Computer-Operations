from networking import Server, WebHandler, AppHandler
import asyncore
import sys
import thread

HOST, PORT = 'localhost', 8888

class Client(AppHandler):
    def on_msg(self, msg):
        print msg
        
def getText():
    while 1:
        mytxt = raw_input("Text: ")
        client.push(client.encode(mytxt) + '\0')
        

client = Client(HOST, PORT)
thread.start_new_thread(getText, ())

asyncore.loop()

