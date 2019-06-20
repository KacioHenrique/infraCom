import socket
HOST = socket.gethostbyname("localhost")  # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dest = (HOST, PORT)
print ('Para sair use CTRL+X\n')
msg = input()
while msg != '\x18':
    udp.sendto (bytes(msg, encoding='latin-1'), dest)
    # udp.sendto (b'vai te tomar no cu kkkkkk', dest)
    msg = input()
    
udp.close()
