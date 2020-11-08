# 
# Sistemas Distribuidos, Proyecto 1
# Programa Maestro.py
# Fecha de creación 7 de noviembre, 2020
# Última modificación: 8 de noviembre, 2020
#
#


import time 
import zmq  
import datetime

#Cantidad de esclavos
Nofslaves = 3
#Lista con las diferencias de tiempo entre maestro y esclavos
dif=[]

context = zmq.Context()
sender = context.socket(zmq.PUSH) 
sender.bind("tcp://*:5557")    
receiver = context.socket(zmq.PULL)
receiver.bind("tcp://*:5558")   

_ = input("Presione enter para comenzar ")

try:
	while True:
		print("\n***************************Iniciando ciclo de sincronización***************************\n")
		#Inicia la solicitud de relojes de los esclavos
		for i in range(Nofslaves):
			msg = "Solicitud de hora"
			#Envía un mensaje para indicar que comienza la sincronización
			sender.send(msg.encode('utf-8'))
			time.sleep(2)
		
		#Obtención de los relojes de los esclavos
		for i in range(Nofslaves):
			#Recibe el reloj del esclavo como string 
			timeString = receiver.recv().decode('utf-8')
			#Convierte el string en un objeto datetime
			clockTime = datetime.datetime.fromisoformat(timeString)
			print("Hora del Maestro: " + str(datetime.datetime.now().time()))
			print("Hora del Esclavo " + str(i) + ": " + str(clockTime.time()))
			#Calcula la diferencia entre el reloj del maestro y el del esclavo
			timeDiff = datetime.datetime.now() - clockTime
			#Agrega la diferencia a una lista
			dif.append(timeDiff)
			time.sleep(2)

		#Calcula el promedio de las diferencias de tiempo de todos los esclavos
		averageTimeDiff = sum(dif, datetime.timedelta(0, 0))/len(dif)
		
		#Envía la actualización de tiempo a todos los esclavos
		for i in range(Nofslaves):
			sender.send(str(averageTimeDiff).encode('utf-8'))
			time.sleep(2)
		
		time.sleep(20)
except KeyboardInterrupt:
	print("Saliendo")
