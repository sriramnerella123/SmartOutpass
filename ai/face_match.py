import cv2
from deepface import DeepFace

# Load Haarcascade for face detection
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# Reference image
reference_img = cv2.imread("c:/Users/SRIRAM/Pictures/Camera Roll/WIN_20260306_07_23_15_Pro.jpg")

# Webcam
cap = cv2.VideoCapture(0)

face_match = False

while True:

    ret, frame = cap.read()
    

    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5,
        minSize=(80,80)
    )

    for (x, y, w, h) in faces:

        face = frame[y:y+h, x:x+w]

        try:
            result = DeepFace.verify(
                face,
                reference_img,
                model_name="Facenet",
                enforce_detection=False
            )

            face_match = result["verified"]

        except:
            face_match = False

        # Draw rectangle
        if face_match:
            color = (0,255,0)
            text = "MATCH"
        else:
            color = (0,0,255)
            text = "NO MATCH"

        cv2.rectangle(frame,(x,y),(x+w,y+h),color,2)
        cv2.putText(frame,text,(x,y-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,color,2)

    cv2.imshow("Face Recognition",frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()