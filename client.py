import socket
import argparse

dnsPort = 53

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

parser = argparse.ArgumentParser()
parser.add_argument('--dnsIP', '-d', type=str, help='IP do DNS para conexão')
parser.add_argument('--hostname', '-h', type=str, help='Nome de server no qual o client quer se conectar')
args = parser.parse_args()

try:
	clientSocket.connect((serverName, serverPort))
except Exception:
	pass
	
try:
	dnsIP = args.dnsIP
	hostname = args.hostname

	if command == "GET" or command == "GETPROG":
		message = command + "-" + contents
	elif command == "POST":
		message = command + '-' + toFile + '-' + contents
		
	clientSocket.send(message.encode()) # send command and contents to server
	print("I send " + message)

	# change path according command
	if command == "GET" or command == "GETPROG":
		path = toFile

		# save contents in output files
		with open(path, "wb") as f:
			data = clientSocket.recv(1024) # receive from server
			while data:
				f.write(data)
				data = clientSocket.recv(1024)
	
		if command == "GETPROG":
			print("running " + path + "\n\n")
			os.system("chmod u+x " + path) # desprotect program
			os.system("./" + path) # run program
		
		clientSocket.close()

except KeyboardInterrupt:
	escape = True
except Exception:
	clientSocket.close()

clientSocket.close()
print("\nClose socket")

