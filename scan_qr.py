import cv2
import pymysql
import os

conn = pymysql.connect(
    host = "localhost",
    user = "root",
    password = "k@nthi123",
    database = "outpass_management"
)
cursor = conn.cursor()
detector = cv2.QRCodeDetector()
cap = cv2.VideoCapture(0)
scanned = False

while True:
    ret,frame = cap.read()
    data,bbox,_ = detector.detectAndDecode(frame)
    
    if data and not scanned:
        scanned = True
        team_id = data.strip()
        print("Qr scanned:",team_id)
        
        query = """
        SELECT Parent_photo
        FROM students
        WHERE Team_id = %s
        LIMIT 1
        """
        
        cursor.execute(query,(team_id,))
        result = cursor.fetchone()
        print("Query Res:",result)
        if result:
            photo_path =result[0]
            base_dir = os.path.dirname(os.path.abspath(__file__))
            full_path = os.path.join(base_dir,photo_path)
            print("Full path:",full_path)
            print("File exists:",os.path.exists(full_path))
            img = cv2.imread(full_path)
            if img is not None: 
               cv2.imshow("Parent Photo",img)
               cv2.waitKey(0)
            else:
                print("Image not found")
        else:
            print("No database record for:",team_id)
                
    cv2.imshow("Qr scanned",frame)
    if cv2.waitKey(1)==27:
        break
cap.release()
cv2.destroyAllWindows()
        
        
        
        