# Importar bibliotecas
import cv2
import mediapipe as mp
from threading import Thread
import time
import numpy as np # Para la creacion del video e imagenes
import datetime

# Usado para convertir el mensaje protobuf en un diccionario.
from google.protobuf.json_format import MessageToDict

# Inicializar el modelo de detección de manos
mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
	model_complexity=1,
	min_detection_confidence=0.75,
	min_tracking_confidence=0.75,
	max_num_hands=2)

# Iniciar la captura de video desde la cámara web
cap = cv2.VideoCapture(0)

# Inicializar contadores y variables
left_counter = 0
right_counter = 0
is_recording = False
photo_taken = False # Variable para que no saque repetidas las fotos

# Función para el temporizador
def timer_function():
    global right_counter, left_counter, photo_taken
    while True:
        time.sleep(1)
        right_counter += 1
        left_counter += 1
        if left_counter == 6:
            left_counter = 0
            photo_taken = False

# Iniciar el temporizador en un hilo separado
timer_thread = Thread(target=timer_function)
timer_thread.daemon = True  # El hilo del temporizador se detendrá cuando el programa principal termine
timer_thread.start()

# Agrega variables para manejar la grabación de video
video_writer = None
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

while True:
	# Leer el cuadro de video
	success, img = cap.read()

	# Voltear la imagen (frame)
	img = cv2.flip(img, 1)

	# Convertir la imagen BGR a RGB
	imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

	# Procesar la imagen RGB
	results = hands.process(imgRGB)

	# Si se detectan manos en la imagen (frame)
	if results.multi_hand_landmarks:

		# Obtiene la fecha y hora actual
		now = datetime.datetime.now()
    	# Formatea la fecha y hora en una cadena legible
		date_time_str = now.strftime("%Y-%m-%d_%H-%M-%S")

		# Se detectan dos manos
		if len(results.multi_handedness) == 2:
				# Display 'Both Hands' on the image
			cv2.putText(img, 'Ambas manos', (250, 50),
						cv2.FONT_HERSHEY_COMPLEX,
						0.9, (0, 255, 0), 2)
			# Reinicia el contador y el video si se detectan ambas
			right_counter = 0
			left_counter = 0
			if is_recording:
				video_writer.release()
				is_recording = False
			
		# Se detecta una sola mano
		else:
			for i in results.multi_handedness:
				
				# Devoluelve si es una mano derecha o izquierda
				etiqueta = MessageToDict(i)['classification'][0]['label']

				if etiqueta == 'Left':
					
					# Mostrar 'Mano Izquierda' en
					# el lado izquierdo de la ventana
					# Si llega a los 5 segundo con la mano levantada sacar foto
					if left_counter == 5 and not photo_taken:
						cv2.putText(img, "FOTO", (250, 50),
								cv2.FONT_HERSHEY_COMPLEX,
								0.9, (0, 0, 250), 2)
						# Captura una imagen cuando el contador llega a 5
						cv2.imwrite(f"hands-assets/imagen{date_time_str}.jpg", img)
						photo_taken = True
					else:
						cv2.putText(img, f"{5 - left_counter} segundos para foto", (200, 50),
									cv2.FONT_HERSHEY_COMPLEX,
									0.9, (0, 255, 0), 2)
					
						
				if etiqueta == 'Right':
					
					# Mostrar 'Mano Derecha'
					# en el lado derecho de la ventana
					if right_counter >= 5:
						cv2.putText(img, f"{right_counter - 5} segs grabando", (200, 50),
								cv2.FONT_HERSHEY_COMPLEX,
								0.9, (0, 0, 250), 2)
						# Comienza la grabación de video cuando el contador llega a 5
						if not is_recording:
							video_writer = cv2.VideoWriter(f"hands-assets/video{date_time_str}.mp4", cv2.VideoWriter_fourcc(*'XVID'), 20.0, (frame_width, frame_height))
							is_recording = True
					else:
						cv2.putText(img, f"{5 - right_counter} segs. para grabar", (200, 50),
								cv2.FONT_HERSHEY_COMPLEX,
								0.9, (0, 255, 0), 2)
					
	else:
		# Reinicia contador si no hay manos a la vista
		right_counter = 0
		left_counter = 0
	
	if is_recording:
		video_writer.write(img)
				

	# Mostrar el video y cuando se presione 'q',
	# cerrar la ventana
	cv2.imshow('Image', img)
	if cv2.waitKey(1) & 0xff == ord('q'):
		break

if is_recording:
    video_writer.release()

# Liberar la cámara y cerrar la ventana
cap.release()
cv2.destroyAllWindows()
