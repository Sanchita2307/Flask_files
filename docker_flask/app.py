from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return {"message": "Hi from docker flask, Sanchita, How're you ?"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug = True) #will enable you to access your applictaion from ip address - http://192.168.0.18:5000/ along with this address- http://127.0.0.1:5000/
    