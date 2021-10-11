from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONG_DBNAME"] = "seminario"
app.config["MONGO_URI"] = "mongodb+srv://dbuser:Mvkvemu7tfb691sS@cluster0.hobus.mongodb.net/seminario?retryWrites=true&w=majority"
db = PyMongo(app).db

@app.route("/", methods=["GET"])
def test():
    return "Conectado"

@app.route("/register/user", methods=["POST"])
def register_user():
    try:
        db.user.insert_one({
            "_id": request.form["document"],
            "name": request.form["name"],
            "email": request.form["email"],
            "surname": request.form["surname"],
            "password": request.form["password"]
        })

        return jsonify({"response":"Created", "code": 201}), 201
    except:
        return jsonify({"response":"Not Found", "code": 404}), 404

@app.route("/register/local", methods=["POST"])
def register_local():
    try:
        db.user.insert_one({
            "_id": request.form["document"],
            "name": request.form["name"],
            "email": request.form["email"],
            "password": request.form["password"]
        })

        return jsonify({"response":"Created", "code": 201}), 201
    except:
        return jsonify({"response":"Not Found", "code": 404}), 404

@app.route("/login/user", methods=["POST"])
def login_user():
    user = db.user.find_one({'_id': request.form["document"], "password": request.form["password"]})
    if user == None:
        return jsonify({"response":"Not Found", "code": 404}), 404
    user.pop("password")
    return jsonify(user), 200

if __name__ == "__main__":
    app.run(port=4032)