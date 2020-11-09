# 
# Sistemas Distribuidos, Proyecto 1
# Programa Maestro.py
# Fecha de creación: 7 de noviembre, 2020
# Última modificación: 8 de noviembre, 2020
#

import time
import zmq
import datetime
import pickle

#Cantidad de esclavos
Nofslaves = int(input("Ingresa el número de esclavos que se desea controlar: "))

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

input("Presione enter para comenzar ")

try:
	while True:
		#Lista con las diferencias de tiempo entre maestro y esclavos
		dif=[]
		#Lista con los ids de los esclavos
		ids=[]

		print("\n****************Iniciando ciclo de sincronización en el maestro****************\n")
		#Inicia la solicitud de relojes de los esclavos
		for i in range(Nofslaves):
			clientId = socket.recv().decode('utf-8')
			ids.append(clientId)
			msg = "Solicitud de hora"
			#Envía un mensaje para indicar que comienza la sincronización
			socket.send(msg.encode('utf-8'))
			time.sleep(0.05)
		
		#Obtención del tiempo maestro
		masterOffset = datetime.timedelta(0)
		masterTime = datetime.datetime.now() + masterOffset
		#Agrega el tiempo maestro la lista de diferencias de tiempos
		dif.append(masterTime - masterTime)
		print("Hora del Maestro: " + str(datetime.datetime.now()))
		#Obtención de los relojes de los esclavos
		for i in range(Nofslaves):
			#Recibe el reloj del esclavo como string 
			timeString = socket.recv()
			#Convierte el string en un objeto datetime
			clockTime = pickle.loads(timeString)
			print("Hora del Esclavo " + str(ids[i]) + ": " + str(clockTime))
			#Calcula la diferencia entre el reloj del maestro y el del esclavo
			timeDiff = masterTime - clockTime
			#Agrega la diferencia a una lista
			dif.append(timeDiff)
			#Solicita al esclavo espere
			socket.send("Espera...".encode('utf-8'))
			time.sleep(0.05)

		#Calcula el promedio de las diferencias de tiempo de todos los esclavos,
		#incluyendo la diferencia con el tiempo del maestro
		averageTimeDiff = sum(dif, datetime.timedelta(0))/len(dif)
		
		#Envía la actualización de tiempo a todos los esclavos
		#Inicia en 1 porque el índice cero corresponde al proceso maestro
		for i in range(1,len(dif)):
			#Recibe la petición para solictar el offset
			socket.recv()
			#El offset de cada esclavo corresponde con
			# offset = tiempoMaster - tiempoEsclavo - averageTimeDiff
			offset = dif[i] - averageTimeDiff
			socket.send(pickle.dumps(offset))
			time.sleep(0.05)
		
		#Se actualiza con el valor del offset usando el mismo criterio que los
		#esclavos
		addTime = dif[0] - averageTimeDiff
		print("Maestro se debe actualizar " + str(addTime))
		updateTime = datetime.datetime.now() + masterOffset + addTime
		print("Hora del Maestro actualizada: " + str(updateTime))

		time.sleep(10)

except KeyboardInterrupt:
	print("Saliendo")
