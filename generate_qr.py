import pymysql
import qrcode

conn = pymysql.connect(
    host = "localhost",
    user = "root",
    password = "k@nthi123",
    database = "outpass_management"
)

cursor = conn.cursor()
query = """
    SELECT DISTINCT Team_id
    FROM students
    WHERE warden_approval = 1
    """
cursor.execute(query)
teams = cursor.fetchall()
for team in teams:
    team_id = team[0]
    qr = qrcode.make(team_id)
    filename = f"qr_{team_id}.png"
    qr.save(filename)
    print("Qr generated for team:",team_id)
conn.close



