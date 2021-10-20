import cv2
import time

haar_file = (cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')

face_cascade = cv2.CascadeClassifier(haar_file)
webcam = cv2.VideoCapture(1)
contador = 0

while True:
    (_, im) = webcam.read()
    grey = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(grey)
    print(len(faces))
    if (len(faces) == 0):
        time.sleep(3)
        contador += 1
    if (contador == 4):
        print("Esto es una alerta")
        print(contador)
        contador = 0
    for (x, y, w, h) in faces:
        cv2.rectangle(im, (x,y), (x+w, y+h), (0, 0, 255), 1)

    cv2.imshow('OpenCV', im)

    
    key = cv2.waitKey(10)
    if key == 27:
        break

haar_file = (cv2.data.haarcascades +'haarcascade_frontalface_default.xml')
face_cascade = cv2.CascadeClassifier(haar_file)
webcam = cv2.VideoCapture(1)
while True:
    (_, im) = webcam.read()
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray)
    print(len(faces))
    
    if (len(faces) == 0):
        time.sleep(3)
        contador += 1
    if (contador == 4):
        print("Esto es una alerta")
        print(contador)
        contador = 0
    for (x, y, w, h) in faces:
        cv2.rectangle(im, (x,y), (x+w, y+h), (0, 255, 0), 1)

    cv2.imshow('OpenCV', im)

    key = cv2.waitKey(10)
    if key == 27:
        break
