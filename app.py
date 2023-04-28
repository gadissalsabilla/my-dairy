from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime

connection_string = "mongodb+srv://test:sparta@cluster0.l8jeyig.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(connection_string)
db = client.dbsparta

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/show_diary", methods = ["GET"])
def show_diary():
    # sample_receive = request.args.get("sample_give")
    # print(sample_receive)
    articles = list(db.diary.find({},{"_id" : False}))
    return jsonify({"articles" : articles})
    
@app.route("/show_diary", methods = ["POST"])
def save_diary():
    # sample_receive = request.form.get("sample_give")
    # print(sample_receive)
    title_receive = request.form.get("title_give")
    content_receive = request.form.get("content_give")
    file = request.files["file_give"]
    profile = request.files["profile_give"]
    extension = file.filename.split(".")[-1]
    extension1 = profile.filename.split(".")[-1]
    today = datetime.now()
    mytime = today.strftime("%Y-%m-%d-%H-%M-%S")
    filename = f"static/post-{mytime}.{extension}"
    profilename = f"static/profile/post-{mytime}.{extension1}"
    file.save(filename)
    profile.save(profilename)
    doc = {
        "file" : filename,
        "profile" : profilename,
        "title" : title_receive,
        "content" : content_receive,
    }
    db.diary.insert_one(doc)

    return jsonify({"message" : "Data saved"})

if __name__ == "__main__":
    app.run("0.0.0.0", port = 5000, debug = True)
