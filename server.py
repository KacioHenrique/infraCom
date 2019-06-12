import socket

class server():
    def __init__(self,dnsPort,dnsIp):
        self.ip = "127.0.0.1"
        self.port = 5000
        self.sock = socket.socket()
        self.sock.connect((self.ip,self.port))
        print("print connect")
        self.connectDns()
        
    def connectDns(self):
        message = input(" -> ")
        while message != 'q':
            self.sock.send(message.encode())
            data = self.sock.recv(1024).decode()
            print ('Received from server: ' + data)
            message = input(" -> ")
        self.sock.close()
        
        
        
server()