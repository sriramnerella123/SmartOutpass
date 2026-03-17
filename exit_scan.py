import cv2
from cryptography.fernet import Fernet
from datetime import datetime
import pymysql
from database import get_connection

def scan_exit(qr_code):
    conn = get_connection()
    detector = cv2.QRCodeDectector()
    cap = cv2.VideoCapture(0)
    while True:
        ret,frame = cap.read()
        data,bbox,_ = detector.detectAndDecode(frame)
        if data:
            print("QR Detected:",data)
            scan_time = datetime.now()
            break
        cv2.imshow("Scan Qr",frame)
        if cv2.waitKey(1) == 27:
            break 
    cap.release()
    cv2.destroyAllWindows()

    key = Fernet.generate_key()
    cipher = Fernet(key)
    decrypted_data = cipher.decrypt(data.encode())
    text = decrypted_data.decode()
    team_id,timestamp = text.split(":")
    qr_gen_time = datetime.strptime(timestamp,"%Y-%m-%d %H:%M:%S")

    cursor = conn.cursor()
    query = """
    SELECT Student_id,Student_name,Student_year,Branch,Student_phone,Parent_phone,Parent_name
    FROM students
    WHERE Team_id = %s
    """
    cursor.execute(query,(team_id,))
    students = cursor.fetchall()
    for s in students:
        query = """ 
        INSERT INTO 
        exit_log(Student_id,Student_name,Student_year,Branch,Student_phone_number,Parent_phone_number,Parent_name,Team_id,exit_time)
        VALUES(%s,%s,%s,%s,%s,NOW())
        """
    cursor.execute(query,(s[0],team_id))
    conn.commit()
    query1 = "SELECT COUNT(*) FROM students WHERE team_id=%s"
    cursor.execute(query1,(team_id,))
    total = cursor.fetchone()[0]
    query2 = "SELECT COUNT(*) FROM exit_log WHERE team_id=%s"
    cursor.execute(query2,(team_id,))
    exited = cursor.fetchone()[0]
    time_diff = scan_time - qr_gen_time
    if time_diff.total_seconds<=86400:
        print("QR Valid - Within 24 hours")
    else:
        print("QR Expired - Access Denied")
        
    if exited==total:
        print("TEAM COMPLETED EXIT")
    else:
        print("Waiting for remainig team members")


