"Импортируем нужные библиотеки"
from ultralytics import YOLO
from deepface import DeepFace
import cv2
import os
import numpy as np
from scipy.spatial.distance import cosine
import requests

"URL нашего Django API, куда отправляем данные"
API_URL = "http://127.0.0.1:8000/api/attendance/"

"Папка, где лежат эталонные фото студентов"
KNOWN_FACES_DIR = "students"
known_embeddings = {}

"Загружаем все эталонные изображения студентов и считаем эмбеддинги"
print("✅ Загружаем лица студентов...")

for filename in os.listdir(KNOWN_FACES_DIR):
    if filename.endswith((".jpg", ".jpeg", ".png")):
        path = os.path.join(KNOWN_FACES_DIR, filename)
        name = os.path.splitext(filename)[0]
        try:
            "Считаем эмбеддинг лица и сохраняем в словарь"
            embedding = DeepFace.represent(img_path=path, model_name="Facenet", detector_backend="opencv")[0]["embedding"]
            known_embeddings[name] = embedding
            print(f"🔹 {name} добавлен в базу.")
        except Exception as e:
            print(f"❌ Ошибка с {filename}: {e}")

print(f"📚 Всего загружено: {len(known_embeddings)} эталонов")

"Загружаем модель YOLO"
model = YOLO("yolov8n.pt")

"Запускаем веб-камеру"
cap = cv2.VideoCapture(0)

print("📷 Камера запущена. Нажми Q для выхода.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    "Делаем предсказание от YOLO"
    results = model(frame)

    for box in results[0].boxes:
        "Получаем координаты рамки для каждого обнаруженного объекта"
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        face = frame[y1:y2, x1:x2]

        try:
            "Считаем эмбеддинг для найденного лица"
            embedding = DeepFace.represent(face, model_name="Facenet", detector_backend="opencv")[0]["embedding"]
            name = "Неизвестен"

            "Сравниваем эмбеддинг с базой"
            for known_name, known_emb in known_embeddings.items():
                distance = cosine(embedding, known_emb)
                if distance < 0.4:
                    name = known_name
                    break

            "Рисуем рамку и имя на видео"
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            "Отправляем имя студента в Django API, если он распознан"
            if name != "Неизвестен":
                response = requests.post(API_URL, json={"student_name": name})
                if response.status_code == 201:
                    print(f"📡 Отправлено в API: {name}")
                else:
                    print(f"⚠️ Ошибка API: {response.status_code} — {response.text}")

        except Exception as e:
            print("⚠️ Ошибка в обработке лица:", e)

    "Отображаем кадр с распознаванием"
    cv2.imshow("🎓 Распознавание студентов", frame)

    "Выход по клавише Q"
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
