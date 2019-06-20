import socket
from DNSManager import DNSManager
from DNSMessageManager import DNSMessageManager
from DNSUtils import *

port = 53
try:
    ip = socket.gethostbyname(socket.gethostname())
except:
    ip = socket.gethostbyname("localhost")

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind((ip,port))

manager = DNSManager()

printf(ip)

printf("dns server running")
while 1: 
    data, address = sock.recvfrom(512)
    
    printf(address)
    printf("id")
    printf(DNSMessageManager.getId(data))
    printf("flags:")
    printf(DNSMessageManager.getFlags(data))
    printAscii(data)
    
    query = DNSMessageManager.getQuery(data)
    printf(query)
    
    hostname = ".".join(query["hostparts"])
    printf(hostname)
    
    host = DNSManager.getHostByName(hostname)
    printf(host)
    
    res = DNSMessageManager.buildResponse(data)
    
    print([hex(a) for a in res])
    
    # sock.accept()
    sock.sendto(res, address)

# id
# 12623