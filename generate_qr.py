import os
import qrcode

def generate_qr(team_id):
    
    data = f"TEAM:{team_id}"
    
    qr = qrcode.make(data)
    
    folder = "Images"
    
    os.makedirs(folder,exist_ok=True)
    
    filename = f"{folder}/qr_{team_id}.png"
    qr.save(filename)
    
    print("Qr generated for team:",team_id)
    return filename



