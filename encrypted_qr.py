import qrcode
from datetime import datetime
from cryptography.fernet import Fernet

team_id = "S789"
result = {"verified":True}
if result["verified"]:
    print("Access Verified")
    
    timestamp  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(timestamp)
    data = f"{team_id}:{timestamp}"
    
    key = Fernet.generate_key()
    cipher = Fernet(key)
    encrypted_data = cipher.encrypt(data.encode())
    qr = qrcode.make(encrypted_data)
    qr.save("encrypted_qr.png")
    print("Encrypted QR Generated")
else:
    print("Access Denied")

    