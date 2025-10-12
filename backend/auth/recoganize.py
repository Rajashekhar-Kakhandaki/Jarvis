import cv2
import os
import time

def AuthenticateFace(timeout_seconds=15, confidence_threshold=150):
    """
    Detects and recognizes a face using LBPH + Haar cascade.
    This version is intentionally LENIENT (low accuracy / easy acceptance).
    Returns 1 if recognized (by the loose rules), 0 if not recognized or timeout.
    """

    flag = 0
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    TRAINER_PATH = os.path.join(BASE_DIR, "trainer", "trainer.yml")
    CASCADE_PATH = os.path.join(BASE_DIR, "haarcascade_frontalface_default.xml")

    # === Load recognizer ===
    try:
        recognizer = cv2.face.LBPHFaceRecognizer_create()
    except Exception as e:
        print("❌ OpenCV face module not available (cv2.face).", e)
        return 0

    if not os.path.exists(TRAINER_PATH):
        print(f"❌ Trainer file not found: {TRAINER_PATH}")
        return 0
    try:
        recognizer.read(TRAINER_PATH)
    except Exception as e:
        print(f"❌ Failed to read trainer file: {e}")
        return 0

    # === Load Haar cascade ===
    faceCascade = cv2.CascadeClassifier(CASCADE_PATH)
    if faceCascade.empty():
        print(f"❌ Haarcascade not loaded from {CASCADE_PATH}")
        return 0

    # label -> name mapping (ensure labels used during training match this)
    names = ['rajashekhar', 'rajshekhar', 'rajashekhar']

    # === Open camera ===
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cam.isOpened():
        print("❌ Camera could not be opened")
        return 0

    # Lower resolution for faster processing
    cam.set(3, 320)
    cam.set(4, 240)

    # compute a small min face size to be permissive
    minW = int(0.05 * cam.get(3))
    minH = int(0.05 * cam.get(4))

    start_time = time.time()

    print("ℹ️  Starting loose face authentication (very permissive). Press ESC to cancel.")

    while True:
        ret, img = cam.read()
        if not ret:
            print("❌ Failed to grab frame")
            break

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Note: equalizeHist is intentionally disabled to reduce recognition robustness:
        # gray = cv2.equalizeHist(gray)

        # Detect faces (very permissive settings)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=1,   # accept more false positives
            minSize=(minW, minH)
        )

        if len(faces) == 0:
            cv2.putText(img, "Looking for face...", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # Crop ROI with bounds safety
            y1 = max(0, y)
            y2 = min(gray.shape[0], y + h)
            x1 = max(0, x)
            x2 = min(gray.shape[1], x + w)
            face_roi = gray[y1:y2, x1:x2]
            if face_roi.size == 0:
                continue

            try:
                id, confidence = recognizer.predict(face_roi)
            except Exception as e:
                # If recognizer fails for some reason, mark as unknown and continue
                print("⚠️ Recognizer predict error:", e)
                confidence = 999.0
                id = -1

            # VERY LOOSE threshold: accept if confidence is less than threshold
            # LBPH returns lower confidence for better matches; higher = worse
            if confidence < confidence_threshold:
                name = names[id] if (0 <= id < len(names)) else "unknown"
                flag = 1
                cv2.putText(img, f"{name} ({confidence:.1f})", (x+5, y-5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                print(f"✅ Recognized (loose) {name} with confidence {confidence:.2f}")
                break
            else:
                # Show as unknown (but still permissive next frames)
                cv2.putText(img, f"Unknown ({confidence:.1f})", (x+5, y-5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.imshow("Face Authentication (LOOSE)", img)

        k = cv2.waitKey(10) & 0xff
        # Stop if ESC pressed or face recognized
        if k == 27 or flag == 1:
            break

        # Stop if timeout reached
        if time.time() - start_time > timeout_seconds:
            print("⏱ Timeout reached. No face recognized.")
            break

    cam.release()
    cv2.destroyAllWindows()
    return flag


