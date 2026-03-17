import pymysql 
def get_connection():
    return pymysql.connect(
        host = "localhost",
        root = "user",
        password = "k@nthi123",
        database = "outpass_management"
        )