import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands() # Передаются параметры: "Статичное изображение(T/F), Максималное кол-во рук, 
                        # минимальная уверенность для обнаруживания, минимальная уверенность для трекинга" (by default = False, 2, 0.5, 0.5)

mpDraw = mp.solutions.drawing_utils  # Модуль mediapipe для рисования  

pTime = 0
cTime = 0

while True:
	success, img = cap.read()

	imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # Перевод картинки из BGR в RGB
	results = hands.process(imgRGB)

	# print(results.multi_hand_landmarks)
	if results.multi_hand_landmarks:
		for handLms in results.multi_hand_landmarks:
			for id, lm in enumerate(handLms.landmark):
				# print(id, lm)
				h, w, c = img.shape # Высота, Ширина, Каналы
				cx, cy = int(lm.x * w), int(lm.y * h) # Определение координат на картинке
				# print(id, cx, cy)

				if id == 8: # Точка 8 - Кончик указательного пальца
				    cv2.circle(img, (cx, cy), 10, (232, 99, 152), cv2.FILLED)   # По координатам точки на руке, рисуем круг

				if id == 12: # Точка 8 - Кончик Среднего пальца
				    cv2.circle(img, (cx, cy), 10, (232, 99, 152), cv2.FILLED)  # По координатам точки на руке, рисуем круг
            

				#cv2.circle(img, (cx, cy), 10, (0, 0, 255), cv2.FILLED) # Нарисовать каждый круг

			mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS) # Нарисовать точки на руке и их соединения

	cTime = time.time()
	fps = 1/(cTime - pTime) # Определение fps
	pTime = cTime

	cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 255), 3) # Размещение нынешнего fps
	cv2.imshow("Image", img)
	cv2.waitKey(1)