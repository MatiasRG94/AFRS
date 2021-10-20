import wiringpi as wiringpi
from time import sleep
import RPI.GPIO as GPIO
import time
import cv2

GPIO.setmode(GPIO.BCM)
GPIO.setup(11, GPIO.IN)
GPIO.setup(5, GPIO.OUT)

TRIG = 2
ECHO = 3
TRIG2 = 4
ECHO2 = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(TRIG2, GPIO.OUT)
GPIO.setup(ECHO2, GPIO.IN)

def alcohol():
	try:
		while True:
			if GPIO.input(11):
				time.sleep(0.1)
				dato = 0
			if GPIO.input(11)!=1:
				dato = 1
				GPIO.output(5, True)
				time.sleep(0.1)
				GPIO.output(5, False)
			return dato
	finally:					
		GPIO.cleanup()
		
def sensor1():
	#print ("Medicion de distancias progreso del primer sensor")
	try:
		while True:
			GPIO.output(TRIG, GPIO.LOW)
			#print ("Esperando a que el primer sensor se estabilice")
			time.sleep(1)
			GPIO.output(TRIG, GPIO.HIGH)
			time.sleep(0.00001)
			GPIO.output(TRIG, GPIO.LOW)
			#print ("Iniciando eco en el primer sensor")
			while True:
				pulso_inicio = time.time()
				if GPIO.input(ECHO) == GPIO.HIGH:
					break
			while True:
				pulso_fin = time.time()
				if GPIO.input(ECHO) == GPIO.LOW:
					break
			duracion = pulso_fin - pulso_inicio
			distancia = (34300 * duracion) / 2
			#print ("Distancia: %.2f cm") % distancia
			if distancia > 20: 
				dist=1
			if distancia < 20:
				dist=0
			return dist
	finally:
		GPIO.cleanup()

def sensor2():
	#print ("Medicion de distancias en progreso del segundo sensor sensor")
	try:
		while True:
			GPIO.output(TRIG2, GPIO.LOW)
			#print ("Esperando a que el segundo sensor se estabilice")
			time.sleep(1)
			GPIO.output(TRIG2, GPIO.HIGH)
			time.sleep(0.00001)
			GPIO.output(TRIG2, GPIO.LOW)
			#print ("Iniciando eco en el segundo sensor")
			while True:
				pulso_inicio = time.time()
				if GPIO.input(ECHO2) == GPIO.HIGH:
					break
			while True:
				pulso_fin = time.time()
				if GPIO.input(ECHO2) == GPIO.LOW:
					break
			duracion = pulso_fin - pulso_inicio
			distancia = (34300 * duracion) / 2
			#print ("Distancia: %.2f cm") % distancia
			if distancia<10:
				dist=0
			if distancia>10:
				dist=1
			return dist
	finally:
		GPIO.cleanup()

def camara1():
	haar_file = (cv2.data.haarcascades +'haarcascade_frontalface_default.xml')
	face_cascade = cv2.CascadeClassifier(haar_file)
	webcam = cv2.VideoCapture(0)
	while True:
		(_, im) = webcam.read()
		gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
		faces = face_cascade.detectMultiScale(gray)
		for (x, y, w, h) in faces:
			cv2.rectangle(im, (x,y), (x+w, y+h), (0, 255, 0), 1)
		cv2.imshow('OpenCV', im)
		key = cv2.waitKey(10)
		if key == 27:
			break

def camara2():
	haar_file = (cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')
	face_cascade = cv2.CascadeClassifier(haar_file)
	webcam = cv2.VideoCapture(0)
	while True:
		(_, im) = webcam.read()
		grey = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
		faces = face_cascade.detectMultiScale(grey)
		for (x, y, w, h) in faces:
			cv2.rectangle(im, (x,y), (x+w, y+h), (0, 0, 255), 1)
		cv2.imshow('OpenCV', im)
		key = cv2.waitKey(10)
		if key == 27:
			break

def alarma():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(18,GPIO.OUT)
	GPIO.output(18, True)


while True:
	alcholimetro=alcohol()
	if alcholimetro == 1:
		alarma()
		print ("Detecto alcohol")

	if alcholimetro == 0:
		print("Sin problemas")

		while True:
			sens1=sensor1()
			if sens1 == 1:
				alarma()
				break

			if sens1 == 0:
				sens2=sensor2()
				if sens2 == 1:
					alarma()
					break
				
				if sens2 == 1:
					break
