import socket
from DNSManager import DNSManager
from DNSMessageManager import DNSMessageManager

port = 53
ip = socket.gethostbyname(socket.gethostname())

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind((ip,port))

manager = DNSManager()

print(ip)

print("dns server running")
while 1: 
    data, address = sock.recvfrom(512)
    print(type(data))
    print(address)
    
    print("id", DNSMessageManager.getId(data))
    print("flags:")
    print(DNSMessageManager.getFlags(data))
    
    # sock.accept()
    sock.sendto(b'200 OK', address)
