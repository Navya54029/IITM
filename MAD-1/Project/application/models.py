from sqlalchemy import null
from .database import db
from flask_login import UserMixin

class User(UserMixin,db.Model):
    __tablename__ = 'user_master'
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_name = db.Column(db.String, unique=True, nullable = False)
    user_email = db.Column(db.String, unique=True)
    user_pwd = db.Column(db.String, nullable = False)
    # cnfrm_pwd = db.Column(db.String, nullable = False)
    sec_question = db.Column(db.String, nullable = False)
    sec_answer = db.Column(db.String, nullable = False)
    created_date = db.Column(db.String)
    modified_date = db.Column(db.String)
    logout_time = db.Column(db.String) 
    trackers = db.relationship("Tracker", backref="User") 
    logs = db.relationship("Logs", backref="User") 
    def get_id(self):
           return (self.user_id)

class Tracker(db.Model):
    __tablename__ = 'tracker_master'
    tracker_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable = False)
    description = db.Column(db.String, nullable = False)
    type = db.Column(db.String, nullable = False)
    settings = db.Column(db.String)
    chart_type = db.Column(db.String)
    created_date = db.Column(db.String)
    modified_date = db.Column(db.String)
    user_id = db.Column(db.Integer,   db.ForeignKey("user_master.user_id"), primary_key=True, nullable=False)
    # trackers = db.relationship("User", secondary="relation_master")

# class Relations(db.Model):
#     __tablename__ = 'relation_master'
#     relation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     user_id = db.Column(db.Integer,   db.ForeignKey("user_master.user_id"), primary_key=True, nullable=False)
#     tracker_id = db.Column(db.Integer,  db.ForeignKey("tracker_master.tracker_id"), primary_key=True, nullable=False) 
#     log_id = db.Column(db.Integer,  db.ForeignKey("log_master.log_id"), primary_key=True, nullable=False)

class Logs(db.Model):
    __tablename__ = 'log_master'
    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    log_time = db.Column(db.String, nullable = False)
    log_time1 = db.Column(db.String) 
    value = db.Column(db.String, nullable = False)
    notes = db.Column(db.String)
    created_date = db.Column(db.String)
    modified_date = db.Column(db.String)
    selected_choice= db.Column(db.String)
    user_id = db.Column(db.Integer,   db.ForeignKey("user_master.user_id"), primary_key=True, nullable=False)
    tracker_id = db.Column(db.Integer,  db.ForeignKey("tracker_master.tracker_id"), primary_key=True, nullable=False) 
    # users = db.relationship("User", secondary="relation_master",overlaps="trackers")
    # trackers = db.relationship("Tracker", secondary="relation_master",overlaps="trackers")

