from flask import Flask,request,jsonify
import pymysql
from generate_qr import generate_qr
app = Flask(__name__)
conn = pymysql.connect(
        host = "localhost",
        root = "user",
        password = "k@nthi123",
        database = "outpass_management"
        )
@app.route("/wardem_approve",methods=["POST"])
def approve_request():
    data = request.json
    team_id = data["team_id"]
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
    WHERE id = %s
    """
    cursor.execute(update_query,(qr_path,student_id))
    conn.commit()
    return jsonify({
      "status":"approved",
      "team_id":team_id,
      "qr":qr_path
    })
if __name__ == "__main__":
  app.run(debug=True)





    
