import RPi.GPIO as GPIO
import time
import numpy as np
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)#adelante
GPIO.setup(11, GPIO.OUT)#derecha
GPIO.setup(13, GPIO.OUT)#izquierda
GPIO.setup(15, GPIO.OUT)#atras
GPIO.setup(29, GPIO.OUT)#Atrapar
GPIO.setup(31, GPIO.OUT)#Dejar lata
GPIO.setup(12, GPIO.IN)#ultrasonico
GPIO.setup(16, GPIO.IN)#desactivar
import cv2

#import serial

#ser=serial.Serial('Com8',9600)

#Iniciamos la camara
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 200)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
GPIO.output(7, False);
while(1):

    #Capturamos una imagen y la convertimos de RGB -> HSV
    _, imagen = cap.read()
    sub = imagen[0:600, 30:170]
    hsv = cv2.cvtColor(sub, cv2.COLOR_BGR2HSV)


    negro_bajos = np.array([35,105,85], dtype=np.uint8)
    negro_altos = np.array([85, 220, 245], dtype=np.uint8)

    #Crear una mascara con solo los pixeles dentro del rango de verdes
    mask = cv2.inRange(hsv, negro_bajos, negro_altos)

    #Encontrar el area de los objetos que detecta la camara
    moments = cv2.moments(mask)
    area = moments['m00']

    if(area > 1000):

        #Buscamos el centro x, y del objeto

        x = int(moments['m10']/moments['m00']) 
        y = int(moments['m01']/moments['m00'])
        areaR=area/1000

        valora=0
        #Mostramos sus coordenadas por pantalla
        if (x<50): GPIO.output(13, True);GPIO.output(11, False);GPIO.output(7, False);GPIO.output(15, False); print ("izquierda")
        if (x>90): GPIO.output(11, True);GPIO.output(7, False);GPIO.output(13, False);GPIO.output(15, False);	print ("derecha")
        if ((x>50)&(x<90)): GPIO.output(7, True);GPIO.output(13, False);GPIO.output(11, False);GPIO.output(15, False); print ("centro")
        if (areaR>1000): print ("Toma la Lata Weee")

		##hey
    	#ser.stopbits()
   		#line = ser.readline();
    	#line2=int(line)
    	#print(line2)

		##
        #ser.write(valora)
        #print( "x = ", x)
        #print ("y = ", y)
        #Dibujamos una marca en el centro del objeto
        cv2.rectangle(sub, (x-20, y-20), (x+40, y+40),(0,0,255), 2)


    #Mostramos la imagen original con la marca del centro y
    #la mascara
    cv2.imshow('mask', mask)
    #cv2.imshow('Camara', imagen)
    cv2.imshow("sub", sub)
    tecla = cv2.waitKey(5) & 0xFF
    if tecla == 27:
        break

cv2.destroyAllWindows()

