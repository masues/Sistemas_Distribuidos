import json 
import time 
import zmq  
from datetime import datetime as dt

def tiempo():
	time = dt.now() 						#Formato 24hr
	hour = []
	hour.append(time.hour)
	hour.append(time.minute)
	hour.append(time.second)
	return hour

def difference(refference,hour):
	difference = []
	for i in range(len(hour)):
		difference.append(refference[i]-hour[i])
	return difference

def toSeconds(hora):
	segundos = 0
	segundos += hora[0] * 3600
	segundos += hora[1] * 60
	segundos += hora[2]
	return segundos

Nofslaves = 1 								#Cantidad de esclavos
dif=[]

context = zmq.Context()
sender = context.socket(zmq.PUSH) 
sender.bind("tcp://*:5557")    
receiver = context.socket(zmq.PULL)
receiver.bind("tcp://*:5558")   

_ = input("Presione enter para comenzar ")

try:
	while True:
		for i in range(Nofslaves):
			msg = "What is your time?"
			sender.send(msg.encode('utf-8'))
		refference = tiempo()							#Se calcula tiempo de referencia actual
		for i in range(Nofslaves):
			message = json.loads(receiver.recv().decode('utf-8'))
			dif.append(difference(message, refference))
			print(refference)
			print(message)
			print(dif) 

		time.sleep(20)
except KeyboardInterrupt:
	print("Saliendo")
