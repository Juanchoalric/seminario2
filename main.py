from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://dbuser:Mvkvemu7tfb691sS@cluster0.hobus.mongodb.net/seminario?retryWrites=true&w=majority"
db = PyMongo(app).db

@app.route("/register", methods=["POST"])
def register_user():
    db.user.insert_one({
        "_id": request.form["document"],
        "name": request.form["name"],
        "surname": request.form["surname"],
        "password": request.form["password"],
    })

    return "Hello world"

@app.route("/login", methods=["POST"])
def login_user():
    user = db.user.find_one({'_id': request.form["document"], "password": request.form["password"]})
    return jsonify(user) 

@app.route("/", methods=["GET"])
def hello_world():
    return "Hello World"
if __name__ == "__main__":
    app.run(port=4032)