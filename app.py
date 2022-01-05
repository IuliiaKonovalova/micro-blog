import os
import datetime
from flask import Flask, render_template, request
if os.path.exists("env.py"):
    import env

from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)

entries = []

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        entry_content = request.form.get("content")
        formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
        entries.append((entry_content, formatted_date))

    entries_with_date = [
        (
            entry[0],
            entry[1],
            datetime.datetime.strptime(entry[1], "%Y-%m-%d").strftime("%b %d")
        )
        for entry in entries
    ]
    return render_template("home.html", entries=entries_with_date)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)