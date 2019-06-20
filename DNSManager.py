import socket

class DNSManager():
    # [String:String]
    servers = dict() 
    
    def __init__(self):
        print("works!")

    def registerIp(self, hostname, ip):
        self.servers[hostname] = ip
    
    def getIp(self, hostname):
        return self.servers.get(hostname, "nil")
        
    @staticmethod
    def getHostByName(hostname):
        # TODO: Implement the local search before the OS search
        try:
            name = socket.gethostbyname(hostname)
        except:
            name = "0.0.0.0"
        return name