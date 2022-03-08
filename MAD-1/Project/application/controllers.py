from ast import Return
from calendar import month
from crypt import methods
from multiprocessing import Value
from turtle import color
from flask import Flask, redirect, request,url_for
from flask import render_template
from flask import current_app as app
from platformdirs import user_data_dir
from application.models import *
from application.api import *
import urllib.request, json
import datetime
from datetime import datetime
import requests
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from datetime import datetime
import matplotlib.pyplot as plt


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/create", methods=["GET", "POST"])
def signup():

    if request.method == "POST":
    
        created_date= datetime.now()
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
        # print(stmt.user_pwd,stmt.user_name)
        if (user_pwd == stmt.user_pwd and user_name == stmt.user_name):
            print("here")
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
        user_data['logout_time']=user_data['logout_time']
        response=requests.get(f"http://127.0.0.1:5000//v1/api/user_trackers/{user_id}")
        user_tracker_details=json.loads(response.text)
        
        #Dates on Dashboard
        dates=[]
        for tracker in user_tracker_details:
            islog=Logs.query.filter_by(tracker_id=tracker['tracker_id']).first()
            #To check if atleast one log is present for a tracker
            if islog:
                last_tracked = Logs.query.filter_by(tracker_id=tracker['tracker_id']).order_by(desc('modified_date')).first()
                # To check if the log has any modified date, if not it will show the last created date of the log
                if last_tracked.modified_date is None:
                    print(last_tracked.created_date)
                    last_created_log =  Logs.query.filter_by(tracker_id=tracker['tracker_id']).order_by(desc('created_date')).first()
                    dates.append(last_created_log.created_date)
                else:
                    dates.append(last_tracked.modified_date)
                # .strftime("%a %d %b %Y, %H:%M:%S %p")
            # this append date of tracker created if there is no log added to tracker
            else:
                last_tracked = tracker['created_date']
                print(type(last_tracked))
                dates.append(last_tracked)
        # print(dates)
        return render_template("dashboard.html",user_data=user_data,user_tracker_details=user_tracker_details,last_tracked=dates)

            

@app.route(("/addtracker/<int:user_id>"), methods=['GET', 'POST'])
def addtracker(user_id):

    if request.method == "POST":

        add_dict = {
            "name" : request.form.get("tname"),
            "description" : request.form.get("desc"),
            "tracker_type" : request.form.get("tracker_type"),
            "chart_type" : request.form.get("chart_type"),
            "settings" : request.form.get("settings")
        }
        # print(add_dict)
        response = requests.post(f"http://127.0.0.1:5000/v1/api/addtracker/{user_id}", data=add_dict)
        print(response)
        return redirect(url_for("dashboard",user_id=user_id))
    return render_template('addtracker.html',user_id=user_id)

@app.route(("/updatetracker/<int:user_id>/<int:tracker_id>"), methods=['GET', 'POST'])
def updatetracker(user_id,tracker_id):
    
    if request.method == "POST":

        add_dict = {
            "name" : request.form.get("tname"),
            "description" : request.form.get("desc"),
            "chart_type" : request.form.get("chart_type"),
            "settings" : request.form.get("settings")
        }
        response = requests.put(f"http://127.0.0.1:5000/v1/api/updatetracker/{user_id}/{tracker_id}", data=add_dict)
        print(response)
        return redirect(url_for("dashboard",user_id=user_id))
    tracker_data = Tracker.query.filter_by(tracker_id=tracker_id).first()
    print(tracker_data.settings)
    
    response=requests.get(f"http://127.0.0.1:5000/v1/api/dashboard/{user_id}")
    user_data=json.loads(response.text)
    return render_template('updatetracker.html',tracker_data=tracker_data,user_data=user_data)



@app.route(("/deletetracker/<int:user_id>/<int:tracker_id>"), methods=['GET', 'POST'])
def deletetracker(user_id,tracker_id):
    response = requests.delete(f"http://127.0.0.1:5000/v1/api/deletetracker/{user_id}/{tracker_id}")
    print(response)
    return redirect(url_for("dashboard",user_id=user_id))


@app.route(("/logevent/<int:user_id>/<int:tracker_id>"), methods=['GET', 'POST'])
def logevent(user_id,tracker_id):

    if request.method == "POST":

        add_log_dict = {
                "log_time" : request.form.get("ltime"),
                "value" : request.form.get("lvalue"),
                "notes" : request.form.get("notes")
            }
        
        add_log_dict["log_time"]=datetime.strptime(add_log_dict["log_time"], '%Y-%m-%dT%H:%M')
        response= requests.post(f"http://127.0.0.1:5000/v1/api/loganewevent/{user_id}/{tracker_id}",data=add_log_dict)
        return redirect(url_for("viewtracker",user_id=user_id,tracker_id=tracker_id))

    return render_template("logevent.html",user_id=user_id,tracker_id=tracker_id)

@app.route(("/updatelog/<int:user_id>/<int:tracker_id>/<int:log_id>"), methods=['GET', 'POST'])
def updatelog(user_id,tracker_id,log_id):

    update_dict = {
        "log_time" : request.form.get("ltime"),
        "value" : request.form.get("lvalue"),
        "notes" : request.form.get("notes")
    }
    # print(update_dict)
    if request.method == "POST":
        response = requests.put(f"http://127.0.0.1:5000/v1/api/update_log_data/{user_id}/{tracker_id}/{log_id}",data=update_dict)
        return redirect(url_for("viewtracker",user_id=user_id,tracker_id=tracker_id))
        
    response=requests.get(f"http://127.0.0.1:5000/v1/api/update_log_data/{user_id}/{tracker_id}/{log_id}")
    update_log_data=json.loads(response.text)
    return render_template("updatelog.html",log_data=update_log_data,user_id=user_id,tracker_id=tracker_id,log_id=log_id)


@app.route(("/deletelog/<int:user_id>/<int:tracker_id>/<int:log_id>"), methods=['GET', 'POST'])
def deletelog(user_id,tracker_id,log_id):
    response = requests.delete(f"http://127.0.0.1:5000/v1/api/deletelog/{user_id}/{tracker_id}/{log_id}")
    print(response)
    return redirect(url_for("viewtracker",user_id=user_id,tracker_id=tracker_id))

@app.route(("/userlogs/<int:user_id>/<int:tracker_id>"), methods=['GET', 'POST'])
def viewtracker(user_id,tracker_id):

    response=requests.get(f"http://127.0.0.1:5000/v1/api/log_data/{user_id}/{tracker_id}")
    log_data=json.loads(response.text)
    last_tracked = Logs.query.order_by(desc('modified_date')).first()
    # print(last_tracked.modified_date)
    # print(log_data)
    tracker_data = Tracker.query.filter_by(tracker_id=tracker_id).first()
    print(tracker_data.type)
    x=[]
    y=[]
    if tracker_data.type == 'Timestamp':
        for log in log_data:
            x.append(log["log_time"])
            y.append(int(log["value"]))
        plt.switch_backend('Agg') 
        plt.figure(figsize=(10, 6))
        plt.tight_layout()

        if tracker_data.chart_type == 'bar':
            plt.title("Barchart of your logs")
            plt.bar(x,height=y,color='mediumaquamarine',width=0.5)
        else:
            plt.title("Trendline of your logs")
            plt.plot(x,y,c='mediumaquamarine',linewidth = '5.5',marker = 'o')
            
        plt.xlabel('Timestamp')
        plt.ylabel('Values')
        plt.xticks(x, rotation=12)
        plt.savefig('static/img/logplot.png',dpi=70,bbox_inches="tight")
        plt.clf()    

    if tracker_data.type == 'Numeric':
        for log in log_data:
            x.append(log["notes"])
            y.append(int(log["value"]))
        print(x,y)
        print(set(x))
        dict_data ={}
        for x in set(x):
            dict_data[x] = 0
        print(dict_data)
        plt.switch_backend('Agg') 
        plt.figure(figsize=(10, 6))
        plt.tight_layout()

        if tracker_data.chart_type == 'bar':
            plt.title("Barchart of your logs")
            plt.bar(x,height=y,color='mediumaquamarine',width=0.5)
        else:
            plt.title("Trendline of your logs")
            plt.plot(x,y,c='mediumaquamarine',linewidth = '5.5',marker = 'o')
            
        plt.xlabel('notes')
        plt.ylabel('Values')
        plt.xticks(x, rotation=12)
        plt.savefig('static/img/logplot.png',dpi=70,bbox_inches="tight")
        plt.clf()  

    return render_template("tracker.html",user_id=user_id,log_data=log_data,tracker_id=tracker_id,last_tracked=last_tracked.modified_date,tracker_data=tracker_data)





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


   
