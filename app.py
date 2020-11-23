from flask import Flask, render_template, redirect, request
import pymongo
import os
from flask_pymongo import PyMongo
import datetime

app = Flask(__name__)
if os.environ.get("MONGO_URI") == None :
    file = open("connection_string.txt","r")
    connection_string = file.read().strip()
    app.config['MONGO_URI']=connection_string
else:
    app.config['MONGO_URI']= os.environ.get("MONGO_URI")
mongo = PyMongo(app)


@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "GET":
        user_note = mongo.db.userNotes.find()
        notes={}
        for x in user_note:
            notes[x["_id"]]= [ x["name"], x["note"], x["time"][0:16] ]
        print (notes)

        return render_template ("index.html", notes = notes)
        
    else:
        name = request.form["name"]
        note = request.form["note"]
        time = str(datetime.datetime.now())
        mongo.db.userNotes.insert_one({"name":name, "note":note, "time":time})
        print (name, note, time)
        return redirect("/")

@app.route("/delete")
def delete():
    note = request.args.get("note")
    mongo.db.userNotes.delete_one({"note":note})
    return redirect ("/")



if __name__ == "__main__":
    app.run()