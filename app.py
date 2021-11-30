from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from datetime import datetime, timedelta
from email_server import Email
import uuid
import json

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
            date = datetime.strptime(data["date"],"%d-%m-%Y")
            time = datetime.strptime(data["time"] ,"%H:%M:%S")
            db.entry.insert_one({
                "_id": uuid.uuid4().hex,
                "user_id": data["user_id"], #documento
                "store_id": data["store_id"],
                "date": str(date.date()),
                "time": str(time.time())
            })
        else:
            return jsonify({"response":"Store Not Found", "code": 404}), 404
        return jsonify({"response":"Created", "code": 201}), 201
    except:
        return jsonify({"response":"Not Found", "code": 404}), 404

@app.route('/entry', methods=["GET"])
def get_entry():
    try:
        data = request.get_json()
        entry = list(db.entry.find({"user_id": request.args.get("user_id")},{"_id": 0, "user_id": 0}))
        for doc in entry:
            store=db.user.find_one({"_id": doc["store_id"]},{"_id":0, "email":0, "password":0})
            doc["store_name"]=store["name"]
        return json.dumps(entry)
    except:
        return jsonify({"response":"Entry Not Found", "code": 404}), 404

@app.route('/notify', methods=["GET"])
def send_notification():
    try:
        data_user_id = request.args.get("user_id")
        entry = list(db.entry.find({"user_id": data_user_id},{"_id": 0}))
        user_notificator = db.user.find_one({"_id": data_user_id})
        user_alert_datetime = user_notificator.get('alert_datetime')
        date_time_now = datetime.now() + timedelta(hours=-3)
        if ((user_alert_datetime) and (date_time_now.timestamp() < (datetime.strptime(user_alert_datetime,"%Y-%m-%d %H:%M:%S.%f") + timedelta(days=14)).timestamp())):
            return jsonify({"response":"User has already notified their contagion", "code": 400}), 400
        for doc in entry:
            date_time = datetime.strptime(str(doc["date"])+' '+str(doc["time"]),"%Y-%m-%d %H:%M:%S")
            minimun_date = date_time_now + timedelta(days=-14)
            if ((date_time_now.timestamp() >= date_time.timestamp()) and (date_time.timestamp() >= minimun_date.timestamp())):
                if (date_time.hour >= 23):
                    date_time_limit = date_time + timedelta(days=1)
                    new_date = datetime.strftime(date_time_limit,"%Y-%m-%d")
                    user_contacts_before = list(db.entry.find({"store_id": doc["store_id"], "date": doc["date"]},{"_id": 0, "store_id": 0}))
                    user_contacts_after = list(db.entry.find({"store_id": doc["store_id"], "date": new_date},{"_id": 0, "store_id": 0}))
                    user_contacts = user_contacts_before + user_contacts_after
                else:
                    user_contacts = list(db.entry.find({"store_id": doc["store_id"], "date": doc["date"]},{"_id": 0, "store_id": 0}))
                date_time_updated_plus = date_time + timedelta(hours=2)
                date_time_updated_minum = date_time + timedelta(hours=-1)
                date_time_timestamp = date_time.timestamp()
                date_time_updated_plus_timestamp = date_time_updated_plus.timestamp()
                date_time_updated_minum_timestamp = date_time_updated_minum.timestamp()
                for user in user_contacts:
                    user_date_time = datetime.strptime(str(user["date"])+' '+str(user["time"]),"%Y-%m-%d %H:%M:%S")
                    user_timestamp = user_date_time.timestamp()
                    if ((user_timestamp>=date_time_timestamp and user_timestamp<=date_time_updated_plus_timestamp and doc["user_id"]!=user["user_id"]) or 
                        (user_timestamp<=date_time_timestamp and user_timestamp>=date_time_updated_minum_timestamp and doc["user_id"]!=user["user_id"])):
                        user_to_notify = db.user.find_one({'_id': user["user_id"]})
                        notification = Email(user_to_notify["email"], str(user["date"]))
                        notification.start_server()
                        notification.make_login()
                        notification.send_message()
                        notification.stop_server()
        db.user.update_one({"_id": data_user_id}, {"$set": {"alert_datetime": str(datetime.now() + timedelta(hours=-3))}})
        return jsonify({"response":"Users notified", "code": 200}), 200
    except:
        return jsonify({"response":"Notification could not be sent", "code": 404}), 404

if __name__ == "__main__":
    app.run(port=4032)