from networking import Server, WebHandler, AppHandler
import thread
import asyncore

HOST_APP, PORT_APP = 'localhost', 8888
HOST_WEB, PORT_WEB = 'localhost', 8888

class AHandler(AppHandler):
    def on_msg(self, msg):
        print msg
        mytxt = raw_input("Text: ")
        self.push(self.encode(mytxt) + '\0')
        
webServer = Server(HOST_WEB, PORT_WEB, WebHandler)
appServer = Server(HOST_APP, PORT_APP, AHandler)

asyncore.loop()

    