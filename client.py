import socket
import json

lastCounter = 0
localArchives = []

## check recv messages
def ifMessageRecvs(lastCounter):
	msg, server = clientSocket.recvfrom(1024)
	msgJSON = json.loads(msg)

	if lastCounter == msgJSON["order"] - 1:
		lastCounter = msgJSON["order"]
		
		if msgJSON["type"] == "archives":
			localArchives = msgJSON["archives"]

	else:
		print("discarded message")
		

def printMenu():
	print("***** MENU *****")
	print("1. Ver lista de arquivos disponíveis no server")
	print("2. Download de arquivo")
	print("3. Encerrar")
	
def printArchives():
	print("***** ARQUIVOS DISPONIVEIS *****")
	for i in localArchives:
		print(i)
	
## main
if __name__ == "__main__":
	counterToSend = 0

	clientSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	
	serverIP = socket.gethostbyname("localhost")  # Endereco IP do Servidor
	serverPort = 5000
	dest = (serverIP, serverPort)
	
	## connection
	connectMessage = {
		"type": "connect", 
		"order": counterToSend
	}
	
	clientSocket.sendto(bytes(json.dumps(connectMessage), encoding='latin-1'), dest)
	counterToSend += 1
	
	printMenu()
	
	while True:
		ifMessageRecvs(lastCounter)

		command = input()
	
		if command == 1:
			printArchives()
		elif command == 2:
			pass
		elif command == 3:
			clientSocket.close()
			print("\nClose socket")
			