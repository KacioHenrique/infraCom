import socket

class Server():
    def __init__(self,dnsPort,dnsIp):
        self.ip = dnsIp
        self.port = dnsPort
        self.connectDns()
        self.connectClient()
    def connectDns(self):
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        sock.connect((self.ip,self.port))
        message = socket.gethostbyname(socket.gethostname()) + " - " + "www.kacio.com"
        sock.send(message.encode())
        data = sock.recv(1024).decode()
        sock.close()
    
    def connectClient(self):
        HOST = '127.0.0.1' 
        PORT = 65432        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    conn.sendall(data)
    
server = Server(53,'172.31.91.59')