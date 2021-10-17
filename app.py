from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from datetime import datetime
import uuid

app = Flask(__name__)
app.config["MONG_DBNAME"] = "seminario"
app.config["MONGO_URI"] = "mongodb+srv://dbuser:Mvkvemu7tfb691sS@cluster0.hobus.mongodb.net/seminario?retryWrites=true&w=majority"
db = PyMongo(app).db

@app.route("/register/user", methods=["POST"])
def register_user():
    try:
        data = request.get_json()
        user = db.user.find_one({"email": data["email"]})
        if user is not None:
            return jsonify({"response":"You are already registered in the app", "code": 400}), 400
        db.user.insert_one({
            "_id": data["document"],
            "name": data["name"],
            "email": data["email"],
            "surname": data["surname"],
            "password": data["password"]
        })
        return jsonify({"response":"Created", "code": 201}), 201
    except Exception as e:
        print(e)
        return jsonify({"response":"Not Found", "code": 404}), 404

@app.route("/register/local", methods=["POST"])
def register_local():
    try:
        data = request.get_json()
        local = db.user.find_one({"email": data["email"]})
        if local is not None:
            return jsonify({"response":"You are already registered in the app", "code": 400}), 400
        db.user.insert_one({
            "_id": uuid.uuid4().hex,
            "name": data["name"],
            "email": data["email"],
            "password": data["password"]
        })

        return jsonify({"response":"Created", "code": 201}), 201
    except Exception as e:
        print(e)
        return jsonify({"response":"Not Found", "code": 404}), 404

@app.route("/login", methods=["POST"])
def login_user():
    data = request.get_json()
    user = db.user.find_one({'email': data["email"], "password": data["password"]})
    if user == None:
        return jsonify({"response":"Not Found", "code": 404}), 404
    user.pop("password")
    return jsonify(user), 200

@app.route("/entry", methods=["POST"])
def register_entry():
    try:
        data = request.get_json()
        local = db.user.find_one({"_id": data["store_id"]})
        if local:
            db.entry.insert_one({
                "_id": uuid.uuid4().hex,
                "user_id": data["user_id"],
                "store_id": data["store_id"],
                "date": datetime.now().strftime("%d-%b-%Y"),
                "time": datetime.now().strftime("%H:%M:%S")
            })
        else:
            return jsonify({"response":"Store Not Found", "code": 404}), 404
        return jsonify({"response":"Created", "code": 201}), 201
    except:
        return jsonify({"response":"Not Found", "code": 404}), 404

@app.route('/entry', methods=["GET"])
def get_entry():
    try:
        entry = db.entry.find_one({"store_id": request.args.get("store_id")})
        return jsonify(entry), 200
    except:
        return jsonify({"response":"Entry Not Found", "code": 404}), 404

if __name__ == "__main__":
    app.run(port=4032)