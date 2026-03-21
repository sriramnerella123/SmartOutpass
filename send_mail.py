import smtplib
from email.message import EmailMessage
from database import get_connection


def send_qr_mail(team_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        SELECT users_data.Email_id
        FROM students
        JOIN users_data 
        ON users_data.Student_id = students.Student_id
        WHERE students.Team_id = %s
        """
    cursor.execute(query,(team_id,))
    emails = cursor.fetchall()

    server = smtplib.SMTP_SSL("smtp.gmail.com",465)
    server.login("rguktoutpass@gmail.com","avar drbn ryuc hkht")
    
    for e in emails:
        msg = EmailMessage()
        msg["Subject"] = "Exit QR Code"
        msg["From"] = "rguktoutpass@gmail.com"
        msg["To"] = e[0]
        msg.set_content("Your team exit Qr code is attached Now You can leave")
    
        with open("encrypted_qr.png","rb") as f:
            file_data = f.read()
        msg.add_attachment(file_data,
                        maintype="image",
                        subtype="png",
                        filename = "exit_qr.png")
        server.send_message(msg)
        server.quit()
        print("QR sent to all members")
    

