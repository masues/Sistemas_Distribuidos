from random import randint as ri
import datetime
import time 
import zmq  

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
		sender.send(str(clientTime).encode('utf-8'))
		#Recibe la cantidad de tiempo, como string, al que debe ajustarse su reloj
		timeDiffString = receiver.recv().decode('utf-8') 
		#Convierte el string en un objeto datetime
		timeDiff = datetime.datetime.strptime(timeDiffString, "%H:%M:%S.%f")
		print("Esclavo 2 se debe actualizar " + str(timeDiff.time()))
		#Objeto timedelta para adicionar la cantidad de tiempo al reloj del esclavo
		addTime = datetime.timedelta(hours = timeDiff.hour,
																 minutes = timeDiff.minute,
																 seconds = timeDiff.second,
																 microseconds = timeDiff.microsecond)
		#Actualiza el reloj del esclavo
		updateTime = datetime.datetime.now() + addTime
		print("Hora del Esclavo 2 actualizada: " + str(updateTime.time()))
except KeyboardInterrupt:
	print("Saliendo")
