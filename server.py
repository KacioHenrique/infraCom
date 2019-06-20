import socket
from ArchiveList import ArchiveList
import json

class Server():
    archiveList = ArchiveList()
    
    def __init__(self,dnsPort,dnsIp):
        self.ip = dnsIp
        self.port = dnsPort
        #self.connectDns()
        self.connectClient()
        
    def connectDns(self):
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        sock.connect((self.ip,self.port))
        message = socket.gethostbyname(socket.gethostname()) + " - " + "www.kacio.com"
        sock.send(message.encode())
        data = sock.recv(1024).decode()
        sock.close()
    
    def connectClient(self):
        HOST = ''
        PORT = 5000
        counter = 0
            
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        orig = (HOST, PORT)
        udp.bind(orig)
        
        while True:
            msg, client = udp.recvfrom(1024)
            msgJSON = json.loads(msg)

            print(client, msgJSON["type"])
            
            if msgJSON["type"] == "connect":
                archives = {
                	"type": "archives", 
                	"archives": self.archiveList.getAllArchives(),
                	"order": counter
                }
                
                udp.sendto(bytes(json.dumps(archives), encoding='latin-1'), client) # send list of files to the connected client
                
            counter += 1
            
        udp.close()
                    
server = Server(0,'')
server.connectClient()
