import os
import datetime
from flask import Flask, render_template, request, redirect
from flask.helpers import url_for
if os.path.exists("env.py"):
    import env

from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/main")
def main():
    entries_with_date = [
        (
            entry["content"],
            entry["data"],
            datetime.datetime.strptime(entry["data"], "%Y-%m-%d").strftime("%b %d")
        )
        for entry in mongo.db.entries.find({}).sort('data', -1)
    ]
    return render_template("main.html", entries=entries_with_date)


@app.route("/add_post", methods=["GET", "POST"])
def add_post():
    # if request.method == "POST":
    #     entry_content = request.form.get("content")
    #     formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
    #     mongo.db.entries.insert_one({"content": entry_content, "data": formatted_date})
    #     return redirect(url_for('main'))
    return render_template("home.html")





if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)