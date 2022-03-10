from flask_sqlalchemy import SQLAlchemy
from jinja2 import Template
from flask_restful import Resource, Api
from flask_restful import *
from flask_restful import marshal_with,fields,reqparse
from matplotlib.cbook import print_cycles
from pkg_resources import get_distribution
from werkzeug.exceptions import HTTPException
from application.models import *
import json
from app import *
from .database import db
import datetime
from flask import Request, jsonify
from application.models import *



api = Api(app)




#Defining output fields using marshal_with
user_output_fields = {
	"user_id" : fields.Integer,
	"user_name" : fields.String,
	"user_email" : fields.String,
	"sec_question" : fields.String,
    "sec_answer" : fields.String,
    "created_date" : fields.String
}

#Defining output fields using marshal_with
user_dashboard_output_fields = {
	"user_id" : fields.Integer,
	"user_name" : fields.String,
	"user_email" : fields.String,
	"sec_question" : fields.String,
    "sec_answer" : fields.String,
    "created_date" : fields.String,
    "modified_date" : fields.String,
    "logout_time" : fields.String
}

#Defining output fields using marshal_with
update_tracker_output_fields = {
	"user_id" : fields.Integer,
    "tracker_id" : fields.Integer,
	"name" : fields.String,
	"type" : fields.String,
	"description" : fields.String,
    "chart_type" : fields.String,
    "settings" : fields.String,
    "modified_date" : fields.String
}

#Defining output fields using marshal_with
tracker_output_fields = {
    "user_id" : fields.Integer,
    "tracker_id" : fields.Integer,
	"name" : fields.String,
	"type" : fields.String,
	"description" : fields.String,
    "chart_type" : fields.String,
    "created_date" : fields.String,
    "settings" : fields.String,
    "modified_date" : fields.String
}

add_log_output_fields = {
    "user_id" : fields.Integer,
    "tracker_id" : fields.Integer,
    "log_id" : fields.Integer,
    "log_time" : fields.String,
    "value" : fields.String,
    "notes" : fields.String,
    "selected_choice" : fields.String,
    "created_date" : fields.String,
    "modified_date" : fields.String
}



#To read values from create tracker request Body
create_tracker_parser = reqparse.RequestParser()
create_tracker_parser.add_argument('name')
create_tracker_parser.add_argument('description')
create_tracker_parser.add_argument('tracker_type',type=str)
create_tracker_parser.add_argument('chart_type',type=str)
create_tracker_parser.add_argument('settings',type=str)

#To read values from create log request Body
create_log_parser = reqparse.RequestParser()
create_log_parser.add_argument('log_time')
create_log_parser.add_argument('value')
create_log_parser.add_argument('notes',type=str)
create_log_parser.add_argument('selected_choice',type=str)

#Define UserCreate API

class USERCREATEAPI(Resource):
    
    @marshal_with(user_output_fields)
    def post(self):
        print("Inside Post")
        json_data = request.get_json(force=True)

        if isinstance(json_data,str):
            json_load = (json.loads(json_data))
            created_date= datetime.datetime.now()
            newuser = User(user_name = json_load["user_name"], user_email = json_load["user_email"], user_pwd = json_load["user_pwd"], cnfrm_pwd= json_load["user_cnfmpwd"],sec_question = json_load["sec_question"],sec_answer = json_load["sec_answer"], created_date = created_date)
        else:
            created_date= datetime.datetime.now()
            newuser = User(user_name = json_data["user_name"], user_email = json_data["user_email"], user_pwd = json_data["user_pwd"], cnfrm_pwd= json_data["user_cnfmpwd"],sec_question = json_data["sec_question"],sec_answer = json_data["sec_answer"], created_date = created_date)
        
        db.session.add(newuser)
        db.session.commit()

        return newuser, 200

    #To send the user data to /profile route
    @marshal_with(user_output_fields)
    def get(self,user_id):
        
        print("Inside Get")
        user = db.session.query(User).filter_by(user_id= user_id).first()
        
        return user,200

    @marshal_with(user_output_fields)
    def put(self,user_id):
        print("Inside Put")
        json_data = request.get_json(force=True)

        if isinstance(json_data,str):
            print("in if")
            json_load = (json.loads(json_data))
            modified_date= datetime.datetime.now()
            edituser = User.query.filter_by(user_id=user_id).update(dict(user_name = json_load["user_name"], user_pwd = json_load["user_pwd1"], cnfrm_pwd= json_load["user_cnfmpwd"],sec_question = json_load["sec_question"],sec_answer = json_load["sec_answer"], modified_date = modified_date))
            
        else:
            print("in else")
            modified_date= datetime.datetime.now()
            edituser = User.query.filter_by(user_id=user_id).update(dict(user_name = json_data["user_name"], user_pwd = json_data["user_pwd1"], cnfrm_pwd= json_data["user_cnfmpwd"],sec_question = json_data["sec_question"],sec_answer = json_data["sec_answer"], modified_date = modified_date))
            edituser1 = User(user_id= user_id,user_name = json_data["user_name"], user_pwd = json_data["user_pwd1"], cnfrm_pwd= json_data["user_cnfmpwd"],sec_question = json_data["sec_question"],sec_answer = json_data["sec_answer"], modified_date = modified_date)
        db.session.commit()
        return edituser1,200

        
class LOGOUTUSERAPI(Resource):
    def get(self,user_id):
        print("Inside Get")
        logout_time = datetime.datetime.now()
        print(type(logout_time))
        user=User.query.filter_by(user_id=user_id).update(dict(logout_time = logout_time))
        db.session.commit()
        return 200

class DASHBOARDAPI(Resource):
    
    @marshal_with(user_dashboard_output_fields)
    def get(self,user_id):
        user_details = User.query.filter_by(user_id=user_id).first()
        return user_details,200


class TRACKERAPI(Resource):
    @marshal_with(tracker_output_fields)
    def get(self,user_id):
        user_tracker_details = Tracker.query.filter_by(user_id=user_id).all()
        print(user_tracker_details)
        return user_tracker_details,200

    @marshal_with(tracker_output_fields)
    def post(self,user_id):
        print("Inside Post")
        args = create_tracker_parser.parse_args()
        print(args)
        add_dict = {
            "tname" : args.get("name",None),
            "desc" : args.get("description",None),
            "tracker_type" : args.get("tracker_type",None),
            "chart_type" : args.get("chart_type", None),
            "settings" : args.get("settings",None)
        }

        created_date=datetime.datetime.now()
        newtracker= Tracker(name=add_dict["tname"],description=add_dict["desc"],type=add_dict["tracker_type"],created_date=created_date,user_id=user_id,settings=add_dict["settings"],chart_type=add_dict["chart_type"])
        db.session.add(newtracker)
        db.session.commit()
        
        return newtracker,200

    @marshal_with(update_tracker_output_fields)
    def put(self,tracker_id,user_id):
        print("Inside PUT")
        print(user_id,tracker_id)
        args = create_tracker_parser.parse_args()
        updatetracker=db.session.query(Tracker).filter_by(tracker_id=tracker_id).first()
        updatetracker.name=args.get("name",None)
        updatetracker.description=args.get("description",None)
        updatetracker.settings=args.get("settings",None)
        updatetracker.chart_type =args.get("chart_type", None)
        updatetracker.modified_date=datetime.datetime.now()
        db.session.commit()
        print(updatetracker)

        return updatetracker,200
    
    def delete(self,tracker_id,user_id):
        print("Inside DELETE")
        deletetracker=Tracker.query.filter_by(user_id=user_id,tracker_id=tracker_id).first()
        db.session.delete(deletetracker)
        db.session.commit()
        return 200


class LOGAPI(Resource):
    
    @marshal_with(add_log_output_fields)
    def get(self,user_id,tracker_id):
        print("Inside GET")
        log_data=Logs.query.filter_by(user_id=user_id,tracker_id=tracker_id).all()
        return log_data,200

    @marshal_with(add_log_output_fields)
    def post(self,user_id,tracker_id):
        print("Inside POST")
        print(user_id,tracker_id)
        args = create_log_parser.parse_args()
        created_date=datetime.datetime.now()
        newlog = Logs(log_time= args.get("log_time",None),value= args.get("value",None),notes= args.get("notes",None),user_id=user_id,tracker_id=tracker_id,created_date=created_date,selected_choice = args.get("selected_choice"))
        db.session.add(newlog)
        db.session.commit()
        return newlog,200



    def delete(self,user_id,tracker_id,log_id):
        print("Inside delete")
        deletelog=Logs.query.filter_by(user_id=user_id,tracker_id=tracker_id,log_id=log_id).first()
        print(deletelog)
        db.session.delete(deletelog)
        db.session.commit()
        return 200

class UPDATEGETAPI(Resource):
    @marshal_with(add_log_output_fields)
    def get(self,user_id,tracker_id,log_id):
        print("Inside GET")
        update_log_data = Logs.query.filter_by(log_id=log_id).first()
        return update_log_data,200
    
    @marshal_with(add_log_output_fields)
    def put(self,user_id,tracker_id,log_id):
        print("INSIDE PUT")
        args = create_log_parser.parse_args()
        # print(args)
        updatelog=db.session.query(Logs).filter_by(log_id=log_id).first()
        updatelog.log_time=args.get("log_time",None)
        updatelog.value=args.get("value",None)
        updatelog.notes=args.get("notes",None)
        updatelog.selected_choice=args.get("selected_choice",None)
        updatelog.modified_date=datetime.datetime.now()
        db.session.commit()
        # print(updatelog)
        return updatelog,200
    
 

# Adding API resources
api.add_resource(USERCREATEAPI,"/v1/api/create","/v1/api/user/<int:user_id>")
api.add_resource(LOGOUTUSERAPI,"/v1/api/logout/<int:user_id>")
api.add_resource(DASHBOARDAPI,"/v1/api/dashboard/<int:user_id>")
api.add_resource(TRACKERAPI,"/v1/api/addtracker/<int:user_id>","/v1/api/user_trackers/<int:user_id>","/v1/api/updatetracker/<int:user_id>/<int:tracker_id>","/v1/api/deletetracker/<int:user_id>/<int:tracker_id>")
api.add_resource(LOGAPI,"/v1/api/loganewevent/<int:user_id>/<int:tracker_id>","/v1/api/log_data/<int:user_id>/<int:tracker_id>","/v1/api/deletelog/<int:user_id>/<int:tracker_id>/<int:log_id>")    
api.add_resource(UPDATEGETAPI,"/v1/api/update_log_data/<int:user_id>/<int:tracker_id>/<int:log_id>")	