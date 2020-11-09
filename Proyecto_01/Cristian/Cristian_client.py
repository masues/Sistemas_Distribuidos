#
# Sistemas Distribuidos, Proyecto 1
# Programa Cristian_client.py
# Fecha de creación: 5 de noviembre, 2020
# Última modificación: 5 de noviembre, 2020
#
#

import json 
from random import randint as ri
from datetime import datetime as dt
import time 
import zmq  

# Función que permite obtener una lista que contiene una hora aleatoria
# Se establece un valor variando los minutos y segundos de la hora actual
def randomHour():
	time = dt.now() 						
	hour = []
	hour.append(time.hour)
	hour.append(time.minute + ri(-4,4))
	hour.append(time.second + ri(-9,9))
	return hour

# Permite dar formato a la lista que representa la hora
def formatHour(hour):
	return str(hour[0])+":"+str(hour[1])+":"+str(hour[2])

try:
	# Lee el archivo que contiene el número de servidores activos
	stream = open("serv.txt", "r") 
	info = stream.readline().split()
	numofserver = info[1]
	stream.close()
except Exception as exc:
	print("No se puede abrir el archivo:", exc)

# Establece el contexto y tipo de socket de ZMQ
context = zmq.Context()
client = context.socket(zmq.REQ)
port = 5557
for i in range(1,int(numofserver)):
	# Conecta con todos los servidores que tenga disponibles
	client.connect("tcp://localhost:"+str(port)) 
	port += 1
solicitud = 0

_ = input("Presione enter solo si ya estan activados todos los clientes...")

try:
	# Reinicia el archivo de servidores para que pueda utilizarse en la siguiente
	# ejecución del programa
	stream = open("serv.txt", "w")  
	stream.write("5557 1")		
	stream.close()
except Exception as exc:
	print("No se puede abrir el archivo:", exc)

try:
	while True:
		_ = input("Presione enter para enviar una solicitud...")
		# Incrementa el contador de solicitudes para mostrarlo en pantalla
		solicitud += 1
		# Obtiene un reloj aleatorio
		hour = randomHour()
		print("Enviando solicitud: "+str(solicitud)+"...")
		for i in range(1,int(numofserver)):
			# Envía la solicitud al servidor
			client.send("What is your hour?".encode('utf-8'))
			# El servidor responde con su hora
			reply = json.loads(client.recv().decode('utf-8'))
			# Imprime la hora actualizada
			print("Hora actual-->"+formatHour(hour)+" Hora actualizada--->"+formatHour(reply)+" del servidor: "+str(reply[3]))
except KeyboardInterrupt:
	print("Saliendo")
