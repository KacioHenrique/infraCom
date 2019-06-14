# https://askubuntu.com/questions/907246/how-to-disable-systemd-resolved-in-ubuntu

import socket
import argparse

clientSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

dnsIP = "172.31.91.59"
dnsPort = 53

try:
	clientSocket.connect((dnsIP, dnsPort))
	print("connect dns")
except Exception as e:
	print(e)
	pass
	
try:
	hostname = input("Hostname? ")

	clientSocket.send(hostname.encode()) # send hostname to server
	serverIP = clientSocket.recv(1024) # receive from server
	print("serverIP = " + str(serverIP))
	
	clientSocket.close()
	clientSocket.connect((dnsIP, dnsPort))
	
	while 1:
		data = clientSocket.recv(1024)

except KeyboardInterrupt:
	escape = True
except Exception as e:
	print(e)
	clientSocket.close()

clientSocket.close()
print("\nClose socket")

