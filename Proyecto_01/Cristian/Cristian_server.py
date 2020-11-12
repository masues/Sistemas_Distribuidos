#
# Sistemas Distribuidos, Proyecto 1
# Programa Cristian_server.py
# Fecha de creación: 5 de noviembre, 2020
# Última modificación: 11 de noviembre, 2020
#
#

import pickle, time, zmq, datetime

# Genera una lista que reperesenta al reloj UTC
def tiempo(server):
	time = datetime.datetime.now()
	hour = []
	hour.append(time)
	hour.append(server)
	return hour

# Función que devuelve el siguiente puerto disponible y el siguiente número de
# servidores
def update(info):
	port = int(info[0])
	port += 1
	number = int(info[1])
	number+= 1
	return str(port)+" "+str(number)

try:
	# Abre el archivo para leer el puerto que corresponde al servidor actual
	# y su número identificador
	stream = open("serv.txt", "r") 
	info = stream.readline().split()
	port = info[0]
	numofserver = info[1] 			#Para identificar a los servidores por número
	stream.close()
except Exception as exc:
	print("No se puede abrir el archivo:", exc)


try:
	# Actualiza la información del siguiente puerto y número de servidores
	# disponibles usando la función update
	stream = open("serv.txt", "w")  
	stream.write(update(info))		
	stream.close()
except Exception as exc:
	print("No se puede abrir el archivo:", exc)

# Establece el socket con el puerto correspondiente a el servidor actual
context = zmq.Context()
server = context.socket(zmq.REP) 
server.bind("tcp://*:"+port)    

_ = input("Presione enter para comenzar...")

try:
	while True:
		# Recibe la petición del client
		msg = server.recv().decode('utf-8')
		# Muestra en pantalla la solicitud del cliente
		print("Solicitud del cliente --> ",msg)
		# Genera una lista con el tiempo UTC del servidor actual
		refference = tiempo(numofserver)
		# Envía la información del del tiempo UTC del servidor actual
		server.send(pickle.dumps(refference))
except KeyboardInterrupt:
	print("Saliendo")
