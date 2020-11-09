# 
# Sistemas Distribuidos, Proyecto 1
# Programa Esclavo.py
# Fecha de creación: 7 de noviembre, 2020
# Última modificación: 8 de noviembre, 2020
#
#

from random import randint as ri
import datetime
import time
import zmq
import pickle

#Obtiene un offset de la hora del esclavo modificando los minutos y segundos
def getRandomOffset():
	return datetime.timedelta(minutes=ri(-10,10), seconds=ri(-30,30))

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

id = str(input("Inserta el identificador del esclavo: "))

try:
	while True:
		print("\n****************Iniciando ciclo de sincronización en el esclavo****************\n")
		#Envia el id
		socket.send(id.encode('utf-8'))
		#Recibe el mensaje para iniciar la sincronización
		message = socket.recv().decode('utf-8')
		print(message)
		time.sleep(1)
		#Obtiene el offset aleatorio del esclavo
		clientOffset = getRandomOffset()
		#Asigna el tiempo al esclavo
		clientTime = datetime.datetime.now() + clientOffset
		print("Hora del esclavo " + id +": "+ str(clientTime))
		#Envía su hora al maestro
		socket.send(pickle.dumps(clientTime))
		#Recibe la señal de espera
		socket.recv()
		time.sleep(1)
		#Envia señal para solicitar el offset
		socket.send("Trae el offset".encode('utf-8'))
		#Recibe la cantidad de tiempo, como string, al que debe ajustarse su reloj
		timeDiffString = socket.recv()
		#Convierte el string en un objeto timedelta para adicionar la cantidad de
		#tiempo al reloj del esclavo
		addTime = pickle.loads(timeDiffString)
		print("Esclavo " + id + " se debe actualizar: " + str(addTime))
		#Actualiza el reloj del esclavo
		updateTime = datetime.datetime.now() + clientOffset + addTime
		print("Hora del Esclavo " + id + " actualizada: " + str(updateTime))
		time.sleep(1)

except KeyboardInterrupt:
	print("Saliendo")
