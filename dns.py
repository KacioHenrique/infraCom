import socket
from DNSManager import DNSManager
from DNSMessageManager import DNSMessageManager

port = 53
ip = socket.gethostbyname(socket.gethostname())


def printf(message):
    with open('log.txt', 'a+') as f:
        f.write(str(message) + "\n")  # Python 3.x

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind((ip,port))

manager = DNSManager()

print(ip)

print("dns server running")
while 1: 
    data, address = sock.recvfrom(512)
    printf(type(data))
    printf(address)
    
    printf("id")
    printf(DNSMessageManager.getId(data))
    printf("flags:")
    printf(DNSMessageManager.getFlags(data))
    
    res = DNSMessageManager.buildResponse(data)
    # sock.accept()
    sock.sendto(res, address)
