import json 
import time 
import zmq  
from datetime import datetime as dt

def tiempo(server):
	time = dt.now() 						
	hour = []
	hour.append(time.hour)
	hour.append(time.minute)
	hour.append(time.second)
	hour.append(server)
	return hour

def update(info):
	port = int(info[0])
	port += 1
	number = int(info[1])
	number+= 1
	return str(port)+" "+str(number)

try:
	stream = open("serv.txt", "r") 
	info = stream.readline().split()
	port = info[0]
	numofserver = info[1] 			#Para identificar a los servidores por número
	stream.close()
except Exception as exc:
	print("No se puede abrir el archivo:", exc)


try:
	stream = open("serv.txt", "w")  
	stream.write(update(info))		
	stream.close()
except Exception as exc:
	print("No se puede abrir el archivo:", exc)

context = zmq.Context()
server = context.socket(zmq.REP) 
server.bind("tcp://*:"+port)    

_ = input("Presione enter para comenzar...")

try:
	while True:
		msg = server.recv().decode('utf-8')
		print("Solicitud del cliente --> ",msg)
		refference = tiempo(numofserver)			
		server.send(json.dumps(refference).encode('utf-8'))				
except KeyboardInterrupt:
	print("Saliendo")
