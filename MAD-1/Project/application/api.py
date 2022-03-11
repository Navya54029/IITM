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
from application.validations import *
import re


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
create_user_parser = reqparse.RequestParser()
create_user_parser.add_argument('user_name')
create_user_parser.add_argument('user_email')
create_user_parser.add_argument('user_pwd',type=str)
create_user_parser.add_argument('user_cnfmpwd',type=str)
create_user_parser.add_argument('sec_question',type=str)
create_user_parser.add_argument('sec_answer',type=str)

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
        args = create_user_parser.parse_args()
        user_dict = {
            "user_name" : args.get("user_name",None),
            "user_email" : args.get("user_email",None),
            "user_pwd" : args.get("user_pwd",None),
            "user_cnfmpwd" : args.get("user_cnfmpwd", None),
            "sec_question" : args.get("sec_question",None),
            "sec_answer" : args.get("sec_answer",None)
        }

        # for validating an Email
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        # To return error responses based on user input
        if user_dict["user_name"] is None or user_dict["user_name"].isnumeric():
            raise BusinessValidationError(status_code=400,error_code="USER001",error_message="Username is required and should be String")
            
        if user_dict["user_email"] is None or not re.fullmatch(regex, user_dict["user_email"]):
            raise BusinessValidationError(status_code=400,error_code="USER002",error_message="Email is required and should be valid")
            
        if user_dict["user_pwd"] is None or user_dict["sec_question"] is None or user_dict["sec_answer"] is None:
            raise BusinessValidationError(status_code=400,error_code="USER003",error_message="Password, Security Question and Answer are required")

        usernameexists = db.session.query(User).filter(User.user_name == user_dict["user_name"]).first()
        # print(usernameexists)
        if usernameexists:
            raise UserExistError(status_code=409)
        # print(user_dict)
        created_date= datetime.datetime.now()
        newuser = User(user_name = user_dict["user_name"], user_email = user_dict["user_email"], user_pwd = user_dict["user_pwd"], cnfrm_pwd= user_dict["user_cnfmpwd"],sec_question = user_dict["sec_question"],sec_answer = user_dict["sec_answer"], created_date = created_date)
    
        db.session.add(newuser)
        db.session.commit()

        return newuser, 200

    #To send the user data to /profile route
    @marshal_with(user_output_fields)
    def get(self,user_id):
        
        print("Inside Get")
        user = db.session.query(User).filter_by(user_id= user_id).first()
        if user:
            return user,200
        #if user doesn't exist in db
        else:
            raise UserNotFoundError(status_code = 404)


    @marshal_with(user_dashboard_output_fields)
    def put(self,user_id):
        print("Inside Put")
        args = create_user_parser.parse_args()
        user_dict = {
            "user_name" : args.get("user_name",None),
            "user_pwd" : args.get("user_pwd",None),
            "user_cnfmpwd" : args.get("user_cnfmpwd", None),
            "sec_question" : args.get("sec_question",None),
            "sec_answer" : args.get("sec_answer",None)
        }
        # print(user_dict)

         # for validating an Email
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        # To return error responses based on user input
        if user_dict["user_name"] is None or user_dict["user_name"].isnumeric():
            raise BusinessValidationError(status_code=400,error_code="USER001",error_message="Username is required and should be String")
              
        if user_dict["user_pwd"] is None or user_dict["sec_question"] is None or user_dict["sec_answer"] is None:
            raise BusinessValidationError(status_code=400,error_code="USER003",error_message="Password, Security Question and Answer are required")

        usernameexists = db.session.query(User).filter(User.user_name == user_dict["user_name"]).first()
        
        if usernameexists:
            raise UserExistError(status_code=409)
        # print(user_dict)
        
        modified_date= datetime.datetime.now()
        edituser = User.query.filter_by(user_id=user_id).update(dict(user_name = user_dict["user_name"], user_pwd = user_dict["user_pwd"], cnfrm_pwd= user_dict["user_cnfmpwd"],sec_question = user_dict["sec_question"],sec_answer = user_dict["sec_answer"], modified_date = modified_date))
        # edituser1 = User(user_id= user_id,user_name = user_dict["user_name"], user_email=user_dict["user_email"],user_pwd = user_dict["user_pwd"], cnfrm_pwd= user_dict["user_cnfmpwd"],sec_question = user_dict["sec_question"],sec_answer = user_dict["sec_answer"], modified_date = modified_date)
        edituser1 = User.query.filter_by(user_id=user_id).first()
        print(edituser1)
        db.session.commit()
        return edituser1,200

        
class LOGOUTUSERAPI(Resource):
    def get(self,user_id):
        print("Inside Get")
        logout_time = datetime.datetime.now()
        print(type(logout_time))
        user=User.query.filter_by(user_id=user_id).update(dict(logout_time = logout_time))
        if user is None:
            raise UserNotFoundError(status_code = 404)
        db.session.commit()
        return 200

class DASHBOARDAPI(Resource):
    
    @marshal_with(user_dashboard_output_fields)
    def get(self,user_id):
        user_details = User.query.filter_by(user_id=user_id).first()
        if user_details is None:
            raise UserNotFoundError(status_code = 404)
        return user_details,200


class TRACKERAPI(Resource):
    @marshal_with(tracker_output_fields)
    def get(self,user_id):
        user_tracker_details = Tracker.query.filter_by(user_id=user_id).all()
        print(user_tracker_details)
        if user_tracker_details == []:
            raise TrackerNotFoundError(status_code = 404)
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
        if add_dict["tname"] is None or add_dict["tname"].isnumeric():
            raise BusinessValidationError(status_code=400,error_code="TRACKER001",error_message="Tracker Name is required and should be String")
        if add_dict["tracker_type"] is None or add_dict["tracker_type"] not in ["MultipleChoice","Numeric","Timestamp"]:
            raise BusinessValidationError(status_code=400,error_code="TRACKER002",error_message="Tracker Type is required and should be one in [MultipleChoice,Numeric,Timestamp]")
        if add_dict["chart_type"] is None or add_dict["chart_type"] not in ["plot","bar"]:
            raise BusinessValidationError(status_code=400,error_code="TRACKER003",error_message="Chart Type is required and should be one in [plot,bar]")
        
        tnameexists = Tracker.query.filter_by(user_id=user_id).first()
        
        if tnameexists.name == add_dict["tname"]:
            raise TrackerExistError(status_code=409)


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
        tnameexists = Tracker.query.filter_by(user_id=user_id).all()
        for t in tnameexists:
            if t.name == args.get("name",None):
                raise TrackerExistError(status_code=409)
        updatetracker=db.session.query(Tracker).filter_by(tracker_id=tracker_id).first()
        updatetracker.name=args.get("name",None)
        updatetracker.description=args.get("description",None)
        updatetracker.settings=args.get("settings",None)
        updatetracker.chart_type =args.get("chart_type", None)
        updatetracker.modified_date=datetime.datetime.now()

        if updatetracker.name is None or updatetracker.name.isnumeric():
            raise BusinessValidationError(status_code=400,error_code="TRACKER001",error_message="Tracker Name is required and should be String")
        if updatetracker.chart_type is None or updatetracker.chart_type not in ["plot","bar"]:
            raise BusinessValidationError(status_code=400,error_code="TRACKER003",error_message="Chart Type is required and should be one in [plot,bar]")
        
        db.session.commit()
        print(updatetracker)

        return updatetracker,200
    
    def delete(self,tracker_id,user_id):
        print("Inside DELETE")
        deletetracker=Tracker.query.filter_by(user_id=user_id,tracker_id=tracker_id).first()
        print(deletetracker)
        if deletetracker is None:
            raise TrackerNotFoundError(status_code=404)
        db.session.delete(deletetracker)
        db.session.commit()
        return 200


class LOGAPI(Resource):
    
    @marshal_with(add_log_output_fields)
    def get(self,user_id,tracker_id):
        print("Inside GET")
        log_data=Logs.query.filter_by(user_id=user_id,tracker_id=tracker_id).all()
        print(log_data)
        if log_data == []:
            raise LogNotFoundError(status_code=404)
        return log_data,200

    @marshal_with(add_log_output_fields)
    def post(self,user_id,tracker_id):
        print("Inside POST")
        print(user_id,tracker_id)
        args = create_log_parser.parse_args()
        
        if args.get("log_time") is None:
            raise BusinessValidationError(status_code=400,error_code="LOG001",error_message="Log Time is required")
        if args.get("notes") is None:
            raise BusinessValidationError(status_code=400,error_code="LOG002",error_message="Notes is required")
        if args.get("value") is None:
            raise BusinessValidationError(status_code=400,error_code="LOG003",error_message="Value is required")

        created_date=datetime.datetime.now()
        newlog = Logs(log_time= args.get("log_time",None),value= args.get("value",None),notes= args.get("notes",None),user_id=user_id,tracker_id=tracker_id,created_date=created_date,selected_choice = args.get("selected_choice"))
        db.session.add(newlog)
        db.session.commit()
        return newlog,200



    def delete(self,user_id,tracker_id,log_id):
        print("Inside delete")
        deletelog=Logs.query.filter_by(user_id=user_id,tracker_id=tracker_id,log_id=log_id).first()
        print(deletelog)
        if deletelog is None:
            raise LogNotFoundError(status_code=404)
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
        print(args)
        log = Logs.query.filter_by(log_id=log_id,user_id=user_id,tracker_id=tracker_id).first()
        print(log)
        if log is None:
            raise LogNotFoundError(status_code=404)
        if args.get("log_time") is None:
            raise BusinessValidationError(status_code=400,error_code="LOG001",error_message="Log Time is required")
        if args.get("notes") is None:
            raise BusinessValidationError(status_code=400,error_code="LOG002",error_message="Notes is required")
        if args.get("value") is None:
            raise BusinessValidationError(status_code=400,error_code="LOG003",error_message="Value is required")
        
        updatelog=db.session.query(Logs).filter_by(log_id=log_id,user_id=user_id,tracker_id=tracker_id).first()
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