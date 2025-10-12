import cv2
import os

# === Setup Paths ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # folder where this script lives
CASCADE_PATH = os.path.join(BASE_DIR, "haarcascade_frontalface_default.xml")
SAMPLES_DIR = os.path.join(BASE_DIR, "samples")

# === Ensure samples directory exists ===
if os.path.isfile(SAMPLES_DIR):
    os.remove(SAMPLES_DIR)  # if "samples" exists as a file, delete it
os.makedirs(SAMPLES_DIR, exist_ok=True)

# === Load Haar Cascade ===
detector = cv2.CascadeClassifier(CASCADE_PATH)
if detector.empty():
    print(f"Error: Haarcascade file not loaded from {CASCADE_PATH}")
    exit()

# === Camera Setup ===
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(3, 640)  # width
cam.set(4, 480)  # height

face_id = input("Enter a Numeric user ID here: ")
print("Taking samples, look at the camera ....... ")
count = 0

# === Capture Loop ===
while True:
    ret, img = cam.read()
    if not ret:
        print("Failed to grab frame")
        break

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, 1.3, 5)
    print("Faces detected:", len(faces))  # debug info

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        count += 1

        file_path = os.path.join(SAMPLES_DIR, f"face.{face_id}.{count}.jpg")
        cv2.imwrite(file_path, gray[y:y + h, x:x + w])

    cv2.imshow("image", img)

    k = cv2.waitKey(100) & 0xff
    if k == 27:  # ESC to stop
        break
    elif count >= 100:  # limit number of samples
        break

print("Samples taken, now closing the program....")
cam.release()
cv2.destroyAllWindows()
