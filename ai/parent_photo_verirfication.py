# import cv2 as cv
# import face_recognition #type:ignore
# import os



# def load_known_faces(folder_path):
#     known_encodings = []
#     known_names = []

#     for filename in os.listdir(folder_path):
#         if filename.lower().endswith(('png','jpg','jpeg','webp','jifi')):
#             img_path = os.path.join(folder_path,filename)
#             image = face_recognition.load_image_file(img_path)
#             encodings = face_recognition.face_encodings(image)

#             if encodings:
#                 known_encodings.append(encodings[0])
#                 known_names.append(os.path.splitext(filename)[0])
#             else:
#                 print(f"[WARNING] No face found in {filename}")

#     return known_encodings,known_names
    

# def run_face_recognition(known_faces_folder):
#     known_encodings,known_names = load_known_faces(known_faces_folder)
#     if not known_encodings:
#         print("[ERROR] No faces loaded.Exiting....")
#         return


#     cap = cv.VideoCapture(0)

#     if not cap.isOpened():
#         print("[ERROR] Could not open webcam.")
#         return
#     print("[INFO] Starting face recognition.press 'q' to quit.")


#     while True:
#         ret,frame = cap.read()

#         if not ret:
#             print("[ERROR] Failed to grab frame.")
#             break

#         small_frame = cv.resize(frame,(0,0),fx=0.25,fy=0.25)
#         rgb_small_frame = cv.cvtColor(small_frame,cv.COLOR_BGR2RGB)

#         face_locations = face_recognition.face_locations(rgb_small_frame, model="cnn")
#         face_encodings = face_recognition.face_encodings(rgb_small_frame,face_locations)


#         for(top,right,bottom,left),face_encoding in zip(face_locations,face_encodings):
#             matches = face_recognition.compare_faces(known_encodings,face_encoding)
#             name = "Unknown"

#             face_distances = face_recognition.face_distance(known_encodings,face_encoding)
#             best_match_index = face_distances.argmin() if len(face_distances) >0 else None


#             if best_match_index is not None and matches[best_match_index]:
#                 name = known_names[best_match_index]
            

#             top *= 4
#             right *=4
#             bottom *=4
#             left *= 4

#             cv.rectangle(frame,(left,top),(right,bottom),(0,255,0),2)
#             cv.rectangle(frame,(left,bottom-35),(right,bottom),(0,255,0),cv.FILLED)
#             cv.putText(frame,name,(left+6,bottom-6),
#                                     cv.FONT_HERSHEY_DUPLEX,0.8,(255,255,255),1)
            
#         cv.imshow('Face recognition',frame)

#         if cv.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv.destroyAllWindows()

# if __name__ == "__main__":
#     run_face_recognition("c:/Users/SRIRAM/Desktop/smart-outpass/static/parent_photos")



# import cv2 as cv
# import face_recognition
# import os
# import numpy as np


# def load_known_faces(folder_path):

#     known_encodings = []
#     known_names = []

#     for filename in os.listdir(folder_path):

#         if filename.lower().endswith(('png','jpg','jpeg','webp','jfif')):

#             img_path = os.path.join(folder_path,filename)

#             image = face_recognition.load_image_file(img_path)

#             # detect face
#             face_locations = face_recognition.face_locations(image)

#             encodings = face_recognition.face_encodings(image,face_locations)

#             if encodings:
#                 known_encodings.append(encodings[0])
#                 known_names.append(os.path.splitext(filename)[0])
#             else:
#                 print(f"[WARNING] No face found in {filename}")

#     return known_encodings,known_names



# def run_face_recognition(known_faces_folder):

#     known_encodings,known_names = load_known_faces(known_faces_folder)

#     if not known_encodings:
#         print("[ERROR] No faces loaded.")
#         return

#     cap = cv.VideoCapture(0)

#     process_this_frame = True

#     while True:

#         ret,frame = cap.read()

#         if not ret:
#             break

#         small_frame = cv.resize(frame,(0,0),fx=0.25,fy=0.25)
#         rgb_small_frame = cv.cvtColor(small_frame,cv.COLOR_BGR2RGB)

#         if process_this_frame:

#             face_locations = face_recognition.face_locations(
#                 rgb_small_frame,
#                 number_of_times_to_upsample=2,
#                 model="hog"
#             )

#             face_encodings = face_recognition.face_encodings(
#                 rgb_small_frame,
#                 face_locations
#             )

#             face_names = []

#             for face_encoding in face_encodings:

#                 face_distances = face_recognition.face_distance(
#                     known_encodings,
#                     face_encoding
#                 )

#                 best_match_index = np.argmin(face_distances)

#                 name = "Unknown"

#                 if face_distances[best_match_index] < 0.50:
#                     name = known_names[best_match_index]

#                 face_names.append(name)

#         process_this_frame = not process_this_frame

#         for (top,right,bottom,left),name in zip(face_locations,face_names):

#             top *= 4
#             right *= 4
#             bottom *= 4
#             left *= 4

#             cv.rectangle(frame,(left,top),(right,bottom),(0,255,0),2)

#             cv.rectangle(frame,(left,bottom-35),(right,bottom),(0,255,0),cv.FILLED)

#             cv.putText(frame,name,(left+6,bottom-6),
#                        cv.FONT_HERSHEY_DUPLEX,0.8,(255,255,255),1)

#         cv.imshow("Face Recognition",frame)

#         if cv.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv.destroyAllWindows()


# if __name__ == "__main__":
#     run_face_recognition("c:/Users/SRIRAM/Desktop/smart-outpass/static/parent_photos")






import cv2 as cv
import face_recognition
import os
import numpy as np


# -------------------------------
# Image Enhancement (for blur)
# -------------------------------
def enhance_image(image):

    image_bgr = cv.cvtColor(image, cv.COLOR_RGB2BGR)

    kernel = np.array([
        [0,-1,0],
        [-1,5,-1],
        [0,-1,0]
    ])

    sharpened = cv.filter2D(image_bgr, -1, kernel)

    enhanced = cv.cvtColor(sharpened, cv.COLOR_BGR2RGB)

    return enhanced


# -------------------------------
# Data Augmentation
# -------------------------------
def augment_image(image):

    augmented_images = []

    augmented_images.append(image)

    # flip
    augmented_images.append(cv.flip(image,1))

    # rotate
    augmented_images.append(cv.rotate(image, cv.ROTATE_90_CLOCKWISE))

    # brighter
    brighter = cv.convertScaleAbs(image, alpha=1.2, beta=30)
    augmented_images.append(brighter)

    # darker
    darker = cv.convertScaleAbs(image, alpha=0.8, beta=-20)
    augmented_images.append(darker)

    return augmented_images


# -------------------------------
# Load Known Faces
# -------------------------------
def load_known_faces(folder_path):

    known_encodings = []
    known_names = []

    for filename in os.listdir(folder_path):

        if filename.lower().endswith(('png','jpg','jpeg','webp','jfif')):

            img_path = os.path.join(folder_path,filename)

            image = face_recognition.load_image_file(img_path)

            # enhance blurred image
            image = enhance_image(image)

            # create augmented images
            images = augment_image(image)

            for img in images:

                face_locations = face_recognition.face_locations(img)

                encodings = face_recognition.face_encodings(img, face_locations)

                if encodings:

                    known_encodings.append(encodings[0])
                    known_names.append(os.path.splitext(filename)[0])

                else:
                    print(f"[WARNING] No face found in {filename}")

    return known_encodings, known_names


# -------------------------------
# Run Face Recognition
# -------------------------------
def run_face_recognition(known_faces_folder):

    known_encodings, known_names = load_known_faces(known_faces_folder)

    if not known_encodings:
        print("[ERROR] No faces loaded.")
        return

    cap = cv.VideoCapture(0)

    if not cap.isOpened():
        print("[ERROR] Could not open webcam.")
        return

    print("[INFO] Face recognition started. Press 'q' to quit.")

    process_this_frame = True

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        small_frame = cv.resize(frame,(0,0),fx=0.25,fy=0.25)
        rgb_small_frame = cv.cvtColor(small_frame, cv.COLOR_BGR2RGB)

        if process_this_frame:

            face_locations = face_recognition.face_locations(
                rgb_small_frame,
                number_of_times_to_upsample=2,
                model="hog"
            )

            face_encodings = face_recognition.face_encodings(
                rgb_small_frame,
                face_locations
            )

            face_names = []

            for face_encoding in face_encodings:

                face_distances = face_recognition.face_distance(
                    known_encodings,
                    face_encoding
                )

                best_match_index = np.argmin(face_distances)

                name = "Unknown"

                if face_distances[best_match_index] < 0.50:
                    name = known_names[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame

        for (top,right,bottom,left), name in zip(face_locations, face_names):

            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv.rectangle(frame,(left,top),(right,bottom),(0,255,0),2)

            cv.rectangle(frame,(left,bottom-35),(right,bottom),(0,255,0),cv.FILLED)

            cv.putText(
                frame,
                name,
                (left+6,bottom-6),
                cv.FONT_HERSHEY_DUPLEX,
                0.8,
                (255,255,255),
                1
            )

        cv.imshow("Face Recognition", frame)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()


# -------------------------------
# Main
# -------------------------------
if __name__ == "__main__":

    run_face_recognition(
        "c:/Users/SRIRAM/Desktop/smart-outpass/static/parent_photos"
    )