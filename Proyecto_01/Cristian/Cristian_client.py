import json 
from random import randint as ri
from datetime import datetime as dt
import time 
import zmq  

def randomHour():
	time = dt.now() 						
	hour = []
	hour.append(time.hour)
	hour.append(time.minute + ri(-4,4))
	hour.append(time.second + ri(-9,9))
	return hour

def formatHour(hour):
	return str(hour[0])+":"+str(hour[1])+":"+str(hour[2])

try:
	stream = open("serv.txt", "r") 
	info = stream.readline().split()
	numofserver = info[1]
	stream.close()
except Exception as exc:
	print("No se puede abrir el archivo:", exc)

context = zmq.Context()
client = context.socket(zmq.REQ) 
port = 5557
for i in range(1,int(numofserver)):
	client.connect("tcp://localhost:"+str(port)) 
	port += 1
solicitud = 0

_ = input("Presione enter solo si ya estan activados todos los clientes...")

try:
	stream = open("serv.txt", "w")  
	stream.write("5557 1")		
	stream.close()
except Exception as exc:
	print("No se puede abrir el archivo:", exc)

try:
	while True:
		_ = input("Presione enter para enviar una solicitud...")
		solicitud += 1
		hour = randomHour()
		print("Enviando solicitud: "+str(solicitud)+"...")
		for i in range(1,int(numofserver)):
			client.send("What is your hour?".encode('utf-8'))
			reply = json.loads(client.recv().decode('utf-8'))
			print("Hora actual-->"+formatHour(hour)+" Hora actualizada--->"+formatHour(reply)+" del servidor: "+str(reply[3]))
except KeyboardInterrupt:
	print("Saliendo")
