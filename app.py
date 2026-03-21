from flask import Flask,request,jsonify
import pymysql
from generate_qr import generate_qr
from send_mail import send_qr_mail
from encrypted_qr import encrypt_qr
from exit_scan import scan_exit
from database import get_connection

app = Flask(__name__)
conn = get_connection()

@app.route("/")
def home():
   return "Hey started"
 
@app.route("/warden_approve",methods=["POST"])
def approve_request():
    data = request.json
    team_id = data["Team_id"]
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    query = """
    SELECT Student_id FROM students
    WHERE team_id = %s AND Parent_photo IS NOT NULL
    LIMIT 1"""
    cursor.execute(query,(team_id,))
    student = cursor.fetchone()
    if not student:
       return jsonify({"status":"error","message":"No parent photo found"})
    student_id = student["Student_id"]
    qr_path = generate_qr(team_id)
    update_query = """
    UPDATE students
    SET qr_code=%s
    WHERE Student_id = %s
    """
    cursor.execute(update_query,(qr_path,student_id))
    conn.commit()
    return jsonify({
      "status":"approved",
      "team_id":team_id,
      "qr":qr_path
    })
    
@app.route("/security_verify",methods=["POST"])
def security_verify():
    data = request.json
    qr_code = data["qr"]
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    query = "SELECT team_id FROM students WHERE qr_code=%s"
    cursor.execute(query,(qr_code,))
    result = cursor.fetchone()
    if not result:
      return jsonify({"status":"invalid qr"})
    team_id = result["team_id"]
    encrypted_qr = encrypt_qr(team_id)
    update_query = """
    UPDATE students
    SET qr_code= %s
    WHERE team_id=%s
    """
    cursor.execute(update_query,(encrypted_qr,team_id))
    conn.commit()
    
    send_qr_mail(team_id,encrypted_qr)
    
    return jsonify({
      "status":"verified",
      "tea_id":team_id,
      "qr":"encrypted_qr",
      "message":"Encrypted QR sent to all team members"
    })
@app.route("/scan_qr",methods=["POST"])
def scan_qr():
    data = request.json
    qr_code = data["qr"]
    if not qr_code:
      return jsonify({"status":"error","message":"QR not provided"})
    result = scan_exit(qr_code)
    if not result:
      return jsonify({"status":"Invalid qr"})
    return jsonify({
      "status":"exit recorded",
      "team_id":result
    })
if __name__ == "__main__":
  app.run(debug=True)