#
# Sistemas Distribuidos, Proyecto 1
# Programa Cristian_client.py
# Fecha de creación: 5 de noviembre, 2020
# Última modificación: 11 de noviembre, 2020
#
#

import pickle, time, zmq, datetime
from random import randint as ri

#Obtiene un offset de la hora del esclavo modificando los minutos y segundos
def getRandomOffset():
	return datetime.timedelta(minutes=ri(-10,10), seconds=ri(-30,30))

#Identificador del cliente
id = str(input("Inserta el identificador del clinte: "))

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

_ = input("Presione enter solo si ya están activados todos los clientes...")

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
		hour = datetime.datetime.now() + getRandomOffset()
		print("Enviando solicitud: "+str(solicitud)+"...")
		for i in range(1,int(numofserver)):
			# Guarda el tiempo en que se envió la petición
			tinicial = datetime.datetime.now()
			#Mensaje de solicitud
			msg = "Petición de hora del cliente " + id
			# Envía la solicitud al servidor
			client.send(msg.encode('utf-8'))
			# El servidor responde con su hora
			reply = pickle.loads(client.recv())
			# Guarda el tiempo en que recibe la respuesta del servidor
			tfinal = datetime.datetime.now()
			# Calcula el tround provocado por los tiempos de ida y vuelta
			tround = tfinal - tinicial
			# El offset es tround / 2
			offset = tround / 2
			# Imprime la hora previa y la actualizada
			print("\n****************Mostrando resultados****************\n")
			print("Offset:                                   "+str(offset))
			print("Hora del cliente previa sincronización:   "+str(hour))
			print("Hora recibida del servidor "+str(reply[1])+":             " +
			  str(reply[0])
			)
			print("Hora actualizada:                         "+str(reply[0]+offset))
except KeyboardInterrupt:
	print("Saliendo")
