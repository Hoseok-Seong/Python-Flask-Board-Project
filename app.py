from bson import ObjectId
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017")
db = client["memo_app"]
memo_collection = db["memos"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/save", methods=["POST"])
def save_memo():
    title = request.form.get("title")
    text = request.form.get("text")

    memo = {"title": title, "text": text}
    result = memo_collection.insert_one(memo)
    memo_id = str(result.inserted_id)

    return jsonify({"memo_id": memo_id})

@app.route("/update", methods=["POST"])
def modify_memo():
    memo_id = request.form.get("memo_id")
    title = request.form.get("title")
    text = request.form.get("text")

    memo = {"title": title, "text": text}
    memo_collection.update_one({"_id": ObjectId(memo_id)}, {"$set": memo})

    return jsonify({"success": True})

@app.route("/delete", methods=["POST"])
def delete_memo():
    memo_id = request.form.get("memo_id")

    memo_collection.delete_one({"_id": ObjectId(memo_id)})

    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True)
