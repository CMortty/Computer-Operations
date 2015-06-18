import asyncore
import socket
import asynchat
import json

class WebHandler(asynchat.async_chat):
    def __init__(self, host, port, sock=None):
        if sock:  # passive side: Handler automatically created by a Listener
            asynchat.async_chat.__init__(self, sock)
        else:  # active side: Handler created manually
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
            asynchat.async_chat.__init__(self, sock)
            self.connect((host, port))  # asynchronous and non-blocking
        self.set_terminator("\r\n\r\n")
        self.buff = []
    
    def collect_incoming_data(self, data):
        self.buff.append(data)
    
    def found_terminator(self):
        self.push("<html><body>Test</body></html>")
        self.close()

    def encode(self, msg):
        # return base64.b64encode(zlib.compress(msg))
        return json.dumps(msg)
    
    def decode(self, msg):
        # return base64.b64decode(zlib.decompress(msg))
        return json.loads(msg)

        
class AppHandler(asynchat.async_chat):
    def __init__(self, host, port, sock=None):
        if sock:  # passive side: Handler automatically created by a Listener
            asynchat.async_chat.__init__(self, sock)
        else:  # active side: Handler created manually
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
            asynchat.async_chat.__init__(self, sock)
            self.connect((host, port))  # asynchronous and non-blocking
        self.set_terminator('\0')
        self.buff = []
    
    def collect_incoming_data(self, data):
        self.buff.append(data)
    
    def found_terminator(self):
        msg = self.decode(''.join(self.buff))
        self.buff = []
        self.on_msg(msg)
    
    def on_msg(self, msg):
        pass
    
    def encode(self, msg):
        # return base64.b64encode(zlib.compress(msg))
        return json.dumps(msg)
    
    def decode(self, msg):
        # return base64.b64decode(zlib.decompress(msg))
        return json.loads(msg)


class Server(asyncore.dispatcher):
    def __init__(self, host, port, handler):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)
        self.host = host
        self.port = port
        self.handler = handler
        
    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print 'Incoming connection from %s' % repr(addr)
            handler = self.handler(self.host, self.port, sock)
            