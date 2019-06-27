import socket
from ArchiveList import ArchiveList
from ServerUtils import ServerUtils
import json
import time

millis_now = lambda: int(round(time.time() * 1000))

class Server():
    archiveList = ArchiveList()

    def __init__(self):
        self.notifyDNS("172.31.91.59", "infra.com")

    def connectClient(self):
        HOST = ''
        PORT = 5001
        counter = 0
            
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp.setblocking(False)
        
        orig = (HOST, PORT)
        udp.bind(orig)
        
        while True:
            try:
                msg, adrss = udp.recvfrom(1024)
                msgJSON = json.loads(msg)
                print("Mensagem recebida:")
                print(msg)
                print()
                
                if msgJSON["type"] == "connect":
                    print("Iniciando envio de arquivos para o cliente...")
                    self.serveData(udp, adrss, "archives", ",".join(self.archiveList.getAllArchives()))
                    print()

                elif msgJSON["type"] == "request":
                    self.serveFile(udp, adrss, msgJSON["value"])
            
                else:
                    error = {
                    	"type": "ERROR",
                    	"ord": 0,
                    	"ordn": 0,
                    	"value": "unordered messages"
                    }
                    
                    ServerUtils.sendJson(udp, adrss, error)
                    
            except:
                pass
            
        udp.close()
    
    
    
    ##################################
    ## Stream Service
    ##################################
    def serveFile(self, connection, address, filename):
        stream = ServerUtils.fileToStream(self.archiveList.solictArchive(filename))
        
        # print(stream)
        print(filename)
        
        self.serveData(connection, address, "archives", stream)
        return True
        
    def serveData(self, connection, address, msgtype, stream, timeout=3000, max_timeout=500):
        n = 0
        oldn = 0

        while n < len(stream):
            package = {
        	    "type": msgtype, 
        	    "ord": n,
        	    "ordn": oldn,
        	    "value": stream[n:n+512]
            }
            
            print("sending:", package)
            
            sent = self.sendWithTimeout(connection, address, package, timeout, max_timeout)
            print("n", n, len(stream))
            # if not sent:
            #     return False
            # else:
            oldn = n
            n += min(512, len(stream) - n)
            print("*n", n, len(stream))
        
        package = {
            "type": "END", 
    	    "ord": n,
    	    "ordn": oldn,
    	    "value": ""
        }
        
        sent = self.sendWithTimeout(connection, address, package, timeout, max_timeout)
        
        if not sent:
            return False
        
        return True
    
    def sendWithTimeout(self, connection, address, package, timeout=500, max_timeout=3000):
        ServerUtils.sendJson(connection, address, package)
        t = millis_now()
        t_total = millis_now()
        res = dict()
        
        print(1)
        while millis_now() - t_total < max_timeout:
            while millis_now() - t < timeout:
                try:
                    ans, addrs = connection.recvfrom(1024)
                    ans = json.loads(ans)
                    print("ans:", ans)
                    if ans["type"] == "ACK":
                        return True
                    if ans["type"] == "ERROR":
                        t = millis_now()
                        t_total = millis_now()
                except:
                    pass
        
        # Failure streamming the file
        print(2)

        if millis_now() - t_total > max_timeout:
            print(3)
            return False
        
        print(4)
        return True
    ##################################
    
    ##################################
    ## DNS Zone
    ##################################
    def notifyDNS(self, dnsip, hostname):
        HOST = socket.gethostbyname("localhost")  # Endereco IP do Servidor
        try:
            HOST = socket.gethostbyname(socket.gethostname())
        except:
            HOST = socket.gethostbyname("localhost")
        
        PORT = 53
        dest = (HOST, PORT)
        command = "UPDATE"
        message = bytes("<>".join([command, hostname, HOST]), encoding="latin-1")
        
        
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp:
            udp.sendto(message, dest)
            print("Update no DNS...")


server = Server()
server.connectClient()
