import decimal
from flask import Flask, redirect, request,url_for,render_template,flash
from flask import current_app as app
from application.models import *
from application.api import *
from datetime import datetime
import requests
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import matplotlib.pyplot as plt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user,login_user,logout_user



@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/create", methods=["GET", "POST"])
def signup():

    if request.method == "POST":
    
        user_dict = {
            "user_name" : request.form.get("uname"),
            "user_email" : request.form.get("uemail"),
            "user_pwd" : request.form.get("psw"),
            "user_cnfmpwd" : request.form.get("psw1"),
            "sec_question" : request.form.get("questions"),
            "sec_answer" : request.form.get("ans")
        }

        user_email = User.query.filter_by(user_email=user_dict['user_email']).first()
        user_name = User.query.filter_by(user_name=user_dict['user_name']).first()
        
        #To check password and confirm passwords match and alert user
        if user_dict['user_pwd'] != user_dict['user_cnfmpwd']:
            flash('Passwords doesn\'t Match', category='error')
        #To check email is valid or not
        elif '@' not in user_dict['user_email']:
            flash('Email is not valid', category='error')
        #To check if user name is numeric
        elif user_dict['user_name'].isnumeric():
            flash('User name should not be numeric', category='error')
        #To check if already user name exists
        elif user_name:
            flash('Username already exists')
        #To check if already user email exists
        elif user_email:
            flash('Email address already exists')
        else:
            #To hash the password and save it in DB
            user_dict['user_pwd'] = generate_password_hash(user_dict['user_pwd'], method='sha256')
            #To create new user
            response_res = requests.post("http://127.0.0.1:5000/v1/api/create", data = user_dict)
            flash('User added successfully')
            return render_template("login.html")
        return redirect(url_for('signup'))
    return render_template("create.html")



@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        
        user_name = request.form.get("uname")
        user_pwd = request.form.get("psw")

        user = User.query.filter_by(user_name=user_name).first()

        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not user or not check_password_hash(user.user_pwd, user_pwd):
            flash('Please check your login details and try again.')
            return redirect(url_for('login')) 
        # if the above check passes, then we know the user has the right credentials
        login_user(user)
        return redirect(url_for("dashboard",user_id=user.user_id))
        
    return render_template("login.html")


@app.route("/logout/<int:user_id>", methods=["GET", "POST"])
@login_required
def logout(user_id):
    logout_user()
    response = requests.get(f"http://127.0.0.1:5000/v1/api/logout/{user_id}")
    print("Loggedout")
    return redirect(url_for("home"))



@app.route("/dashboard/<int:user_id>", methods=['GET', 'POST'])
@login_required
def dashboard(user_id):
    
        response=requests.get(f"http://127.0.0.1:5000/v1/api/dashboard/{user_id}")
        user_data=json.loads(response.text)
        user_data['logout_time']=user_data['logout_time']
        responsetrackers=requests.get(f"http://127.0.0.1:5000//v1/api/user_trackers/{user_id}")
        # print(responsetrackers.status_code)
        if responsetrackers.status_code == 404:
            print("Inside if")
            return render_template("dashboard.html",user_data=user_data)
        else:
            user_tracker_details=json.loads(responsetrackers.text)
            
            #Dates on Dashboard
            dates=[]
           
            for tracker in user_tracker_details:
                # print(tracker)
                islog=Logs.query.filter_by(tracker_id=tracker['tracker_id']).first()
                # print(islog)
                #To check if atleast one log is present for a tracker
                if islog is not None:
                    # print("inside is log")
                    last_tracked = Logs.query.filter_by(tracker_id=tracker['tracker_id']).order_by(desc('modified_date')).first()
                    # To check if the log has any modified date, if not it will show the last created date of the log
                    if last_tracked.modified_date is None:
                        # print(last_tracked.created_date)
                        last_created_log =  Logs.query.filter_by(tracker_id=tracker['tracker_id']).order_by(desc('created_date')).first()
                        dates.append(last_created_log.created_date)
                    else:
                        dates.append(last_tracked.modified_date)
                    
                # this append date of tracker created if there is no log added to tracker
                else:
                    last_tracked = tracker['created_date']
                    # print(type(last_tracked))
                    dates.append(last_tracked)
                # print(dates)
            print(current_user.user_name)
            return render_template("dashboard.html",user_data=user_data,user_tracker_details=user_tracker_details,last_tracked=dates,name=current_user.user_name)
            
            

@app.route(("/addtracker/<int:user_id>"), methods=['GET', 'POST'])
@login_required
def addtracker(user_id):

    if request.method == "POST":

        add_dict = {
            "name" : request.form.get("tname"),
            "description" : request.form.get("desc"),
            "tracker_type" : request.form.get("tracker_type"),
            "chart_type" : request.form.get("chart_type"),
            "settings" : request.form.get("settings")
        }
        print(add_dict)
        
        # To check if user has the same tracker name already
        user_tracker_names=Tracker.query.filter_by(name=add_dict['name'],user_id=user_id).first()
        if user_tracker_names:
            flash('Tracker Already Exist.Try another Name')
        #To check if tracker name is numeric
        elif add_dict['name'].isnumeric():
            flash('Tracker Name should not be numeric')
        else:  
            response = requests.post(f"http://127.0.0.1:5000/v1/api/addtracker/{user_id}", data=add_dict)
            return redirect(url_for("dashboard",user_id=user_id))
        return redirect(url_for('addtracker',user_id=user_id))
    return render_template('addtracker.html',user_id=user_id)

@app.route(("/updatetracker/<int:user_id>/<int:tracker_id>"), methods=['GET', 'POST'])
@login_required
def updatetracker(user_id,tracker_id):
    
    if request.method == "POST":

        add_dict = {
            "name" : request.form.get("tname"),
            "description" : request.form.get("desc"),
            "chart_type" : request.form.get("chart_type"),
            "settings" : request.form.get("settings")
        }

        #To check if tracker name is numeric
        if add_dict['name'].isnumeric():
            flash('Tracker Name should not be numeric')
            return redirect(url_for('updatetracker',user_id=user_id,tracker_id=tracker_id))

        response = requests.put(f"http://127.0.0.1:5000/v1/api/updatetracker/{user_id}/{tracker_id}", data=add_dict)
        
        return redirect(url_for("dashboard",user_id=user_id,name=current_user.user_name))

    # GET method code
    tracker_data=Tracker.query.filter_by(tracker_id=tracker_id).first()
    response=requests.get(f"http://127.0.0.1:5000/v1/api/dashboard/{user_id}")
    user_data=json.loads(response.text)

    return render_template('updatetracker.html',tracker_data=tracker_data,user_data=user_data,name=current_user.user_name)



@app.route(("/deletetracker/<int:user_id>/<int:tracker_id>"), methods=['GET', 'POST'])
@login_required
def deletetracker(user_id,tracker_id):
    #To delete the tracker data
    response = requests.delete(f"http://127.0.0.1:5000/v1/api/deletetracker/{user_id}/{tracker_id}")
    response=requests.get(f"http://127.0.0.1:5000/v1/api/log_data/{user_id}/{tracker_id}")
    
    if response.status_code != 404:
        log_data=json.loads(response.text)
        print(log_data)
        #To delete the logs for the tracker
        for log in log_data:
            response = requests.delete(f"http://127.0.0.1:5000/v1/api/deletelog/{user_id}/{tracker_id}/{log['log_id']}")

    return redirect(url_for("dashboard",user_id=user_id,name=current_user.user_name))


@app.route(("/logevent/<int:user_id>/<int:tracker_id>"), methods=['GET', 'POST'])
@login_required
def logevent(user_id,tracker_id):

    if request.method == "POST":

        add_log_dict = {
                "log_time" : request.form.get("ltime"),
                "value" : request.form.get("lvalue"),
                "notes" : request.form.get("notes"),
                "selected_choice" : request.form.get("multiple_type")
            }
        print(add_log_dict)
        def isfloat(num):
            try:
                float(num)
                return True
            except ValueError:
                return False
        if not isfloat(add_log_dict['value']):
            flash('Value should be numeric')
            return redirect(url_for('logevent',user_id=user_id,tracker_id=tracker_id))
        
        add_log_dict["log_time"]=datetime.strptime(add_log_dict["log_time"], '%Y-%m-%dT%H:%M')
        response= requests.post(f"http://127.0.0.1:5000/v1/api/loganewevent/{user_id}/{tracker_id}",data=add_log_dict)
        return redirect(url_for("viewtracker",user_id=user_id,tracker_id=tracker_id,name=current_user.user_name))
    
    #To display Multiple choice values on screen
    tracker_data = Tracker.query.filter_by(tracker_id=tracker_id).first()
    # print(tracker_data.type)
    multiple_data=[]
    if tracker_data.type == "MultipleChoice":
        for d in tracker_data.settings.split(","):
            multiple_data.append(d)

    return render_template("logevent.html",user_id=user_id,tracker_id=tracker_id,multiple_data=multiple_data,tracker_data=tracker_data,name=current_user.user_name)

@app.route(("/updatelog/<int:user_id>/<int:tracker_id>/<int:log_id>"), methods=['GET', 'POST'])
@login_required
def updatelog(user_id,tracker_id,log_id):

    if request.method == "POST":

        update_dict = {
        "log_time" : request.form.get("ltime"),
        "value" : request.form.get("lvalue"),
        "notes" : request.form.get("notes"),
        "selected_choice" : request.form.get("multiple_type")
        }
        # print(update_dict)
        def isfloat(num):
            try:
                float(num)
                return True
            except ValueError:
                return False
        if not isfloat(update_dict['value']):
                flash('Value should be numeric')
                return redirect(url_for('updatelog',user_id=user_id,tracker_id=tracker_id,log_id=log_id))
        update_dict['log_time'] = datetime.strptime(update_dict["log_time"], '%Y-%m-%dT%H:%M')
        response = requests.put(f"http://127.0.0.1:5000/v1/api/update_log_data/{user_id}/{tracker_id}/{log_id}",data=update_dict)
        # print(response.text)
        return redirect(url_for("viewtracker",user_id=user_id,tracker_id=tracker_id,name=current_user.user_name))
        
    response=requests.get(f"http://127.0.0.1:5000/v1/api/update_log_data/{user_id}/{tracker_id}/{log_id}")
    update_log_data=json.loads(response.text)
    tracker_data = Tracker.query.filter_by(tracker_id=tracker_id).first()
    print(tracker_data.type)
    multiple_data=[]
    for d in tracker_data.settings.split(","):
        multiple_data.append(d)
    # print(update_log_data)
    return render_template("updatelog.html",log_data=update_log_data,user_id=user_id,tracker_id=tracker_id,log_id=log_id,tracker_data=tracker_data,multiple_data=multiple_data,name=current_user.user_name)


@app.route(("/deletelog/<int:user_id>/<int:tracker_id>/<int:log_id>"), methods=['GET', 'POST'])
@login_required
def deletelog(user_id,tracker_id,log_id):
    response = requests.delete(f"http://127.0.0.1:5000/v1/api/deletelog/{user_id}/{tracker_id}/{log_id}")
    # print(response)
    return redirect(url_for("viewtracker",user_id=user_id,tracker_id=tracker_id,name=current_user.user_name))

@app.route(("/userlogs/<int:user_id>/<int:tracker_id>"), methods=['GET', 'POST'])
@login_required
def viewtracker(user_id,tracker_id):

    response=requests.get(f"http://127.0.0.1:5000/v1/api/log_data/{user_id}/{tracker_id}")
    print(response.status_code)
    
    tracker_data = Tracker.query.filter_by(tracker_id=tracker_id).first()
    islog=Logs.query.filter_by(tracker_id=tracker_id).count()
    if response.status_code==404:
        
        return render_template("tracker.html",user_id=user_id,tracker_id=tracker_id,tracker_data=tracker_data,islog=islog,name=current_user.user_name)
    else:
        log_data=json.loads(response.text)
        last_tracked = Logs.query.order_by(desc('modified_date')).first()
        # print(last_tracked.modified_date)
        
        tracker_data = Tracker.query.filter_by(tracker_id=tracker_id).first()
        # print(tracker_data.type)
        x=[]
        y=[]
        if tracker_data.type == 'Timestamp':
            for log in log_data:
                x.append(log["log_time"])
                y.append(float(log["value"]))   
        
        dict_data={}
        if tracker_data.type == 'Numeric':
            for log in log_data:
                x.append(log["notes"])
                y.append(float(log["value"])) 
            
            for data in list(zip(x, y)):
                if data[0] in dict_data.keys():
                    dict_data[data[0]]+=data[1]
                else:
                    dict_data[data[0]]=data[1]
            
            x=[key for key in dict_data.keys()]
            y=[val for val in dict_data.values()]


        if tracker_data.type == 'MultipleChoice':
            for log in log_data:
                x.append(log["selected_choice"])
                y.append(float(log["value"]))
            # print(list(zip(x,y)))
            for data in list(zip(x,y)):
                if data[0] in dict_data.keys():
                    dict_data[data[0]]+=data[1]
                else:
                    dict_data[data[0]]=data[1]
            # print(dict_data) 
            x=[key for key in dict_data.keys()]
            y=[val for val in dict_data.values()]


        plt.switch_backend('Agg') 
        plt.figure(figsize=(10, 6))
        plt.tight_layout()

        if tracker_data.chart_type == 'bar':
            plt.title("Barchart of your logs")
            plt.bar(x,height=y,color='mediumaquamarine',width=0.3)
        else:
            plt.title("Trendline of your logs")
            plt.plot(x,y,c='mediumaquamarine',linewidth = '5.5',marker = 'o')
            
        plt.xlabel('Notes')
        plt.ylabel('Values')
        plt.xticks(x, rotation=12)
        plt.savefig('static/img/logplot.png',dpi=70,bbox_inches="tight")
        plt.clf()  

    return render_template("tracker.html",user_id=user_id,log_data=log_data,tracker_id=tracker_id,last_tracked=last_tracked.modified_date,tracker_data=tracker_data,islog=islog,name=current_user.user_name)





@app.route("/profile/<int:user_id>", methods=['GET', 'POST'])
@login_required
def user_profile(user_id):
    user_profile = requests.get(f"http://127.0.0.1:5000/v1/api/user/{user_id}")
    user_data=json.loads(user_profile.text)
    # print(user_data)
    if request.method == "GET":
        return render_template("myprofile.html",user_data=user_data,name=current_user.user_name)

    if request.method == "POST":

        user_dict = {
            "user_pwd" : request.form.get("new"),
            "user_pwd1" : request.form.get("old"),
            "user_cnfmpwd" : request.form.get("new_cnfm"),
            "sec_question" : request.form.get("questions"),
            "sec_answer" : request.form.get("ans")
        }
        # print(user_dict)
        if user_dict['user_pwd'] != user_dict['user_cnfmpwd']:
            flash("New Password and Confirm Password doesn't match.")
        elif not check_password_hash(user_data['user_pwd'], user_dict['user_pwd1']):
            flash("Old Password is incorrect. Please try again")
        else:
            user_dict['user_pwd'] = generate_password_hash(user_dict['user_pwd'], method='sha256')
            user_update = requests.put(f"http://127.0.0.1:5000/v1/api/user/{user_id}", data = user_dict)
            flash("Profile updated successfully")
            return redirect(url_for('dashboard',user_id=user_id))
        return redirect(url_for('user_profile',user_id=user_id))

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')


   
