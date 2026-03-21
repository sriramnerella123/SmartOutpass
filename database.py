import pymysql 
def get_connection():
    return pymysql.connect(
        host = "localhost",
        user = "root",
        password = "k@nthi123",
        database = "outpass_management"
        )
