import socket
from ArchiveList import ArchiveList
import json
import time

millis_now = lambda: int(round(time.time() * 1000))

class Server():
    archiveList = ArchiveList()

    def __init__(self,dnsPort,dnsIp):
        self.ip = dnsIp
        self.port = dnsPort
        #self.connectDns()
        self.connectClient()
        
    def connectDns(self):
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        sock.connect((self.ip,self.port))
        message = socket.gethostbyname(socket.gethostname()) + " - " + "www.kacio.com"
        sock.send(message.encode())
        data = sock.recv(1024).decode()
        sock.close()
    
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
                print(msg)
                
                if msgJSON["type"] == "connect":
                    archives = {
                    	"type": "archives", 
                    	"archives": self.archiveList.getAllArchives()
                    }
                    print(archives)
                    self.send_message(udp, adrss, archives)
                    #udp.sendto(bytes(json.dumps(archives), encoding='latin-1'), adrss) # send list of files to the connected client

                elif msgJSON["type"] == "request":
                        print("solicitando")
                        img = {
                    	    "type": "request", 
                    	    "img":  Imagem(self.archiveList.solictArchive(msgJSON["request"])).getImagem()
                        }
                        print(img)
                        self.send_message(udp, adrss, img)
                        #udp.sendto(bytes(path, encoding='latin-1'), adrss) # send list of files to the connected client
                
                else: # unordered msg
                    error = {
                    	"type": "ERROR"
                    }
                    
                    self.send_message(udp, adrss, error)
                    # udp.sendto(bytes(json.dumps(error), encoding='latin-1'), adrss) # send list of files to the connected client

            except:
                pass
            
        udp.close()
        
    def send_message(self, socket, dest, msg):
    	'''
    	Uma interface de envio de mensagem de stream,
    	assumindo que a stream pode ter um tamanho qualquer.
    	
    		param socket         Socket aberto para trafego UDP
    		param dest           Informações sobre o host de destino
    		param msgList        Uma mensagem que deve ser enviada para o server.
    		                     Esta mensagem deve ser um JSON contendo a informação
    		                     desejada de envio.
    		
    		returns              Uma tupla (status, respostas) com uma lista de
    		                     respostas do servidor para cada um dos pacotes
    		                     enviados pelo client.
    	'''
    	
    	MAX_TIMEOUT = 20000
    	TIMEOUT = 1000
    	begin = millis_now()
    	time = millis_now()
    	
    	resend = False
    	recv = False
    	recvFirst = False
    	msgCount = 0
    	
    	timer = 0
    	ans = []
    	
    	# send message
    	socket.sendto(bytes(json.dumps(msg), encoding='latin-1'), dest)
    	
    	while not recv:
    		# quebra aqui caso passe muito tempo sem receber mensagens
    		if millis_now() - begin > MAX_TIMEOUT:
    			break
    		
    		elif millis_now() - time <= TIMEOUT:
    			try:
    				msg, server = socket.recvfrom(1024)
    				msgJSON = json.loads(msg)
    				
    				# TODO: Check every message type, if error message then resend, 
    				# otherwise, then go over the new package and threat it
    				# no tipo de mensagem de "acabou" aí fecha o loop
    				if msgJSON["type"] == "ERROR":
    					resend = True
    				else:
    					ans += [msgJSON]
    				
    			    # mensagem de tudo certo
    				if msgJSON["type"] == "OK":
    					recv = True
    				
    				if msgJSON["type"] == "END":
    					recv = True
    				
    				# TODO: verificar a ordem dos ACKs
    				ackMessage = {
    					"type": "ACK",
    					"ord": ans[-2]["ord"],
    					"ordn": ans[-1]["ord"],
    					"value": "OK"
    				}
    				recvFirst = True
    				socket.sendto(bytes(json.dumps(ackMessage), encoding='latin-1'), dest)
    				begin = millis_now()
    				
    			except:
    				pass
    			
    		if millis_now - time > TIMEOUT or not resend: # pacote perdido reenvia
    			if not recvFirst:
    				socket.sendto(bytes(json.dumps(msg), encoding='latin-1'), dest)
    				time = millis_now()
    				resend = False
    				
    			else:
    				# caso tenha dado timeout no server mas ja tenha começado o stream
    				ackMessage = {
    					"type": "ACK",
    					"ord": ans[-2]["ord"],
    					"ordn": ans[-1]["ord"],
    					"value": "OK"
    				}
    				socket.sendto(bytes(json.dumps(ackMessage), encoding='latin-1'), dest)
    				time = millis_now()
    				resend = False
    	
    	return recv, ans
                    
server = Server(0,'')
server.connectClient()
