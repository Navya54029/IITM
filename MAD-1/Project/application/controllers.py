from crypt import methods
from flask import Flask, redirect, request,url_for
from flask import render_template
from flask import current_app as app
from platformdirs import user_data_dir
from application.models import *
from application.api import *
import urllib.request, json
import datetime
import requests
from flask_sqlalchemy import SQLAlchemy
from pyhtml import *

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/create", methods=["GET", "POST"])
def signup():

    if request.method == "POST":
    
        created_date= datetime.datetime.now()
        user_dict = {
            "user_name" : request.form.get("uname"),
            "user_email" : request.form.get("uemail"),
            "user_pwd" : request.form.get("psw"),
            "user_cnfmpwd" : request.form.get("psw1"),
            "sec_question" : request.form.get("questions"),
            "sec_answer" : request.form.get("ans")
        }
        user_json_object = json.dumps(user_dict, indent = 4)
    
        print(user_json_object)
        
        response_res = requests.post("http://127.0.0.1:5000/v1/api/create", json = user_json_object)
        return render_template("login.html")
    return render_template("create.html")



@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        
        user_name = request.form.get("uname")
        user_pwd = request.form.get("psw")
        stmt = db.session.query(User).filter_by(user_name= user_name).first()
       
        if (user_pwd == stmt.user_pwd and user_name == stmt.user_name):
            return redirect(url_for("dashboard",user_id=stmt.user_id))
        else:
            return render_template("login.html")
        
    return render_template("login.html")


@app.route("/logout/<int:user_id>", methods=["GET", "POST"])
def logout(user_id):

    response = requests.get(f"http://127.0.0.1:5000/v1/api/logout/{user_id}")
    print("Loggedout")
    return redirect(url_for("home"))



@app.route("/dashboard/<int:user_id>", methods=['GET', 'POST'])
def dashboard(user_id):
    response=requests.get(f"http://127.0.0.1:5000/v1/api/dashboard/{user_id}")
    user_data=json.loads(response.text)
    user_data['logout_time']=user_data['logout_time'].split("-")[0]
    return render_template("dashboard.html",user_data=user_data)
        

@app.route(("/addtracker/<int:user_id>"), methods=['GET', 'POST'])
def addtracker(user_id):

    if request.method == "POST":

        add_dict = {
            "tname" : request.form.get("tname"),
            "desc" : request.form.get("desc"),
            "tracker_type" : request.form.get("tracker_type")
        }
        response = requests.post(f"http://127.0.0.1:5000/v1/api/addtracker/{user_id}", data=add_dict)
        print(response)
        # print(response.text)
        return redirect(url_for("dashboard",user_id=user_id))
    return render_template('addtracker.html',user_id=user_id)






@app.route("/profile/<int:user_id>", methods=['GET', 'POST'])
def user_profile(user_id):

    if request.method == "GET":

        user_profile = requests.get(f"http://127.0.0.1:5000/v1/api/user/{user_id}")
        user_data=json.loads(user_profile.text)
        return render_template("myprofile.html",user_data=user_data)

    if request.method == "POST":

        user_dict = {
            "user_name" : request.form.get("uname"),
            "user_pwd" : request.form.get("old"),
            "user_pwd1" : request.form.get("new"),
            "user_cnfmpwd" : request.form.get("new_cnfm"),
            "sec_question" : request.form.get("questions"),
            "sec_answer" : request.form.get("ans")
        }
        user_json_object = json.dumps(user_dict, indent = 4)
    
        print(user_json_object)
        
        user_update = requests.put(f"http://127.0.0.1:5000/v1/api/user/{user_id}", json = user_json_object)
       
        return render_template("user_profile_update.html", user_id=user_id)


   
