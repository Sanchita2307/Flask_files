from flask import Flask, jsonify

import psycopg2

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(host = "localhost", database = "mydb", 
                            user = "postgres", password = "admin" ) # password we creaed using image at cmd

@app.route("/users")
def get_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("select * from users;")
    rows = cur.fetchall()

    cur.close()
    conn.close()
    users = [{"id": r[0], "name":r[1]} for r in rows] #list comprehension as it returns tuple
    return jsonify(users)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 5000)