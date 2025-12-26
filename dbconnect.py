import mysql.connector

def get_connection():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="root123",   # YOUR MySQL password
            database="student_db",
            port=3307             # IMPORTANT
        )
        return conn
    except mysql.connector.Error as err:
        print("❌ Database Error:", err)
        return None
