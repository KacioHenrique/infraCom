import socket
#because dns lising in this port 
port = 53
ip = '127.0.0.1'
#AF_INET is model ipv4 and ipv6 
#SOCK_DGRAM is udp protocol 
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#recive a tuple (ip,tuple)
sock.bind((ip,port))
while 1: 
    #recvfrom return tupla (bytes,address)
    data,addres = sock.recvfrom(512)
    print(data)
    