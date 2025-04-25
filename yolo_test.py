"Импортируем библиотеки: YOLO от Ultralytics и OpenCV"
from ultralytics import YOLO
import cv2

"Загружаем предобученную модель YOLOv8 (наименьшую по размеру — yolov8n.pt)"
model = YOLO("yolov8n.pt")

"Открываем видеопоток с веб-камеры (устройство 0)"
cap = cv2.VideoCapture(0)

"Основной цикл: считываем кадры и обрабатываем"
while True:
    ret, frame = cap.read()
    if not ret:
        break

    "Передаём кадр в YOLO и получаем результат детекции"
    results = model(frame)

    "Добавляем на изображение рамки и подписи"
    annotated_frame = results[0].plot()

    "Показываем результат в окне"
    cv2.imshow("YOLO Детекция", annotated_frame)

    "Проверяем, нажата ли клавиша 'q' — если да, выходим из цикла"
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

"Освобождаем ресурсы: закрываем камеру и окно"
cap.release()
cv2.destroyAllWindows()
