# 
# Sistemas Distribuidos, Proyecto 1
# Programa Esclavo1.py
# Fecha de creación: 7 de noviembre, 2020
# Última modificación: 8 de noviembre, 2020
#
#

from random import randint as ri
import datetime
import time
import zmq
import pickle

#Obtiene la hora del esclavo modificando los minutos y segundos
#Se realiza la modificación para obtener una variación en la hora respecto al maestro
def randomHour():
	time = datetime.datetime.now() 						
	time.minute + ri(-1,1)
	time.second + ri(-5,5)
	return time

context = zmq.Context()
receiver = context.socket(zmq.PULL) 
receiver.connect("tcp://localhost:5557") 
sender = context.socket(zmq.PUSH)
sender.connect("tcp://localhost:5558") 

try:
	while True:
		#Recibe el mensaje para iniciar la sincronización
		message = receiver.recv().decode('utf-8')
		print(message)
		#Asigna el tiempo al esclavo
		clientTime = randomHour()
		#Envía su hora al maestro
		sender.send(pickle.dumps(clientTime))
		#Recibe la cantidad de tiempo, como string, al que debe ajustarse su reloj
		timeDiffString = receiver.recv() 
		#Convierte el string en un objeto timedelta para adicionar la cantidad de
		#tiempo al reloj del esclavo
		addTime = pickle.loads(timeDiffString)
		print("Esclavo 1 se debe actualizar " + str(addTime))
		#Actualiza el reloj del esclavo
		updateTime = datetime.datetime.now() + addTime
		print("Hora del Esclavo 1 actualizada: " + str(updateTime.time()))
except KeyboardInterrupt:
	print("Saliendo")
