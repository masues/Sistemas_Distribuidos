#Berkeley
import json 
from random import randint as ri
from datetime import datetime as dt
import time 
import zmq  


def randomHour():
	time = dt.now() 						
	hour = []
	hour.append(time.hour)
	hour.append(time.minute + ri(-1,1))
	hour.append(time.second + ri(-5,5))
	return hour

context = zmq.Context()
receiver = context.socket(zmq.PULL) 
receiver.connect("tcp://localhost:5557") 
sender = context.socket(zmq.PUSH)
sender.connect("tcp://localhost:5558") 



try:
	while True:
		hour = randomHour()
		message = receiver.recv().decode('utf-8')
		print(message)
		sender.send(json.dumps(hour).encode('utf-8'))
		
except KeyboardInterrupt:
	print("Saliendo")
