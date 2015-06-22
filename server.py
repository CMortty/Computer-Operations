from networking import Server, WebHandler, AppHandler
import thread
import asyncore
from django.template import Template, Context, loader
from django.conf import settings
from django.http import HttpResponse

HOST_APP, PORT_APP = 'localhost', 8888
HOST_WEB, PORT_WEB = 'localhost', 9999
# HOST_COMM, PORT_COMM = 'localhost', 9998
connections = {}
NAME = "!name!"
ALL = "!all!"
settings.configure( TEMPLATE_DIRS=("templates/",) )

def updateWebsite():
    
    t = loader.get_template('index.html')
#     settings.configure()
#     t = Template('My name is {{ my_name }}.')
    c = Context({'data': connections})
    site = t.render(c)
    web = str(site)
#     print web
    print type(web)
    return web

website = updateWebsite()

class WHandler(WebHandler):
    def on_msg(self, msg):
        statusCode = "HTTP/1.1 200 OK\r\n"
        end = "\r\n"
        responseHeader = statusCode + end
        self.push(responseHeader)
        self.push(website)

class AHandler(AppHandler):
    def on_msg(self, msg):
        global website
        if NAME in msg:
            name = msg.split(NAME)
            if name[1] not in connections.keys():
                connections[name[1]] = self
                website = updateWebsite()
        elif ALL in msg:
            for k in connections.keys():
                self.push(msg.split(ALL)[1])
        
        print msg
    
#         mytxt = raw_input("Text: ")
#         self.push(self.encode(mytxt) + '\0')
        
webServer = Server(HOST_WEB, PORT_WEB, WHandler)
appServer = Server(HOST_APP, PORT_APP, AHandler)

asyncore.loop()
