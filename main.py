import json
from flask import Flask, Response, request
from bson import json_util
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config[
    "MONGO_URI"] = "mongodb+srv://chainAI:chain.ai@clusterrevenuechain.wi8m2.mongodb.net/consumer?retryWrites=true&w=majority"
mongo = PyMongo(app)


@app.route("/", methods=["GET"])
def base():
    return Response(response=json.dumps({"status": "ok"}),
                    status=200,
                    mimetype="application/json")


@app.route("/signUP/consumers", methods=["POST"])
def signUp():
    data = mongo.db.users

    userName = request.json["userName"]
    mobNo = request.json["mobNo"]
    nidNo = request.json["nidNo"]
    walletId = request.json["walletId"]
    amount = request.json["amount"]
    pin = request.json["pin"]

    # check user existing Status using two fields mobile number and nid number

    existingStatus = data.find_one({"mobNo": {"$eq": mobNo}, "nidNo": {"$eq": nidNo}})
    output = str(existingStatus)

    if mobNo and nidNo in output:
        return "user already exist"
    else:
        createProfile = data.insert_one({"userName": userName, "mobNo": mobNo, "nidNo": nidNo,
                                         "walletId": walletId, "amount": amount,
                                         "pin": pin})
        # output = {'Status': 'Successfully Inserted', 'Document_ID': str(createProfile.inserted_id)}
        output = json_util.dumps(createProfile.inserted_id)

        return output


@app.route("/signIn/consumers", methods=["POST"])
def signIn():
    data = mongo.db.users

    mobNo = request.json["mobNo"]
    pin = request.json["pin"]

    # check user existing Status using two fields mobile number and nid number

    existingStatus = data.find_one({"mobNo": {"$eq": mobNo}, "pin": {"$eq": pin}}, {"_id": 0})
    output = json_util.dumps(existingStatus)

    if mobNo and pin in output:
        return output
    else:
        return "incorrect"


@app.route("/getProfile/consumers", methods=["POST"])
def getProfile():
    data = mongo.db.users

    mobNo = request.json["mobNo"]
    existingStatus = data.find_one({"mobNo": {"$eq": mobNo}}, {"_id": 0})
    output = json_util.dumps(existingStatus)

    return output


@app.route("/resetPin/consumers", methods=["POST"])
def resetPin():
    data = mongo.db.users

    mobNo = request.json["mobNo"]
    nidNo = request.json["nidNo"]
    pin = request.json["pin"]

    myQuery = {"mobNo": mobNo, "nidNo": nidNo}
    newValues = {"$set": {"pin": pin}}

    up_data = data.update_one(myQuery, newValues)

    output = str(up_data.modified_count)

    return output


@app.route("/sendMoney/to/consumers", methods=["PUT"])
def sendMoney():
    data = mongo.db.users

    walletId = request.json["walletId"]
    amount = request.json["amount"]

    up_data = data.update_one({"walletId": walletId}, {"$inc": {"amount": amount}})

    # existingStatus = data.find_one({"walletId": {"$eq": walletId}}, {"_id": 0})
    output = str(up_data.modified_count)

    return output


@app.route("/updateBalance/to/consumers", methods=["PUT"])
def updateBalance():
    data = mongo.db.users

    walletId = request.json["walletId"]
    amount = request.json["amount"]

    up_data = data.update_one({"walletId": walletId}, {"$inc": {"amount": amount}})

    # existingStatus = data.find_one({"walletId": {"$eq": walletId}}, {"_id": 0})
    output = str(up_data.modified_count)

    return output


@app.route("/transactionHistory/of/consumers", methods=["POST"])
def transactionHistoryOfConsumers():
    data = mongo.db.transactionHistoryOfConsumers

    dateTime = request.json["dateTime"]
    receiver = request.json["receiver"]
    amount = request.json["amount"]
    sender = request.json["sender"]

    createProfile = data.insert_one({"dateTime": dateTime, "receiver": receiver, "amount": amount,
                                     "sender": sender})
    # output = {'Status': 'Successfully Inserted', 'Document_ID': str(createProfile.inserted_id)}
    output = json_util.dumps(createProfile.inserted_id)

    return output


@app.route("/fetch/transactionHistory/of/consumers", methods=["POST"])
def fetchTransactionHistoryOfConsumers():
    data = mongo.db.transactionHistoryOfConsumers

    sender = request.json["sender"]
    existingStatus = data.find({"sender": {"$eq": sender}}, {"_id": 0})
    output = json_util.dumps(existingStatus)

    return output


if __name__ == '__main__':
    app.run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
