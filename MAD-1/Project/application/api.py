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
    "created_date" : fields.DateTime
}

#Defining output fields using marshal_with
user_dashboard_output_fields = {
	"user_id" : fields.Integer,
	"user_name" : fields.String,
	"user_email" : fields.String,
	"sec_question" : fields.String,
    "sec_answer" : fields.String,
    "created_date" : fields.DateTime,
    "modified_date" : fields.DateTime,
    "logout_time" : fields.DateTime
}


# #To read values from create student POST request Body
# create_user_parser = reqparse.RequestParser()
# create_user_parser.add_argument('user_name')
# create_user_parser.add_argument('user_email')
# create_user_parser.add_argument('user_pwd')
# create_user_parser.add_argument('user_cnfmpwd')
# create_user_parser.add_argument('sec_question')
# create_user_parser.add_argument('sec_answer')
# create_user_parser.add_argument('created_date')


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
        user=User.query.filter_by(user_id=user_id).update(dict(logout_time = logout_time))
        db.session.commit()
        return 200

class DASHBOARDAPI(Resource):
    
    @marshal_with(user_dashboard_output_fields)
    def get(self,user_id):
        user_details = User.query.filter_by(user_id=user_id).first()
        
        return user_details,200

class ADDTRACKERAPI(Resource):
    def get(self):
        return 200

    def post(self,user_id):
        print("Inside Post")
        add_dict = {
            "tname" : request.form.get("tname"),
            "desc" : request.form.get("desc"),
            "tracker_type" : request.form.get("tracker_type")
        }
        print(add_dict)

        
        return 200



# Adding API resources
api.add_resource(USERCREATEAPI,"/v1/api/create","/v1/api/user/<int:user_id>")
api.add_resource(LOGOUTUSERAPI,"/v1/api/logout/<int:user_id>")
api.add_resource(DASHBOARDAPI,"/v1/api/dashboard/<int:user_id>")
api.add_resource(ADDTRACKERAPI,"/v1/api/addtracker/<int:user_id>")
    
	