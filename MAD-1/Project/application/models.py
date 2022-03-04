from sqlalchemy import null
from .database import db

class User(db.Model):
    __tablename__ = 'user_master'
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_name = db.Column(db.String, unique=True, nullable = False)
    user_email = db.Column(db.String, unique=True)
    user_pwd = db.Column(db.String, nullable = False)
    cnfrm_pwd = db.Column(db.String, nullable = False)
    sec_question = db.Column(db.String, nullable = False)
    sec_answer = db.Column(db.String, nullable = False)
    created_date = db.Column(db.DateTime) 
    modified_date = db.Column(db.DateTime)
    logout_time = db.Column(db.DateTime)  

class Tracker(db.Model):
    __tablename__ = 'tracker_master'
    tracker_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable = False)
    description = db.Column(db.String, nullable = False)
    type = db.Column(db.String, nullable = False)
    settings = db.Column(db.String)
    user_id = db.Column(db.Integer,   db.ForeignKey("user_master.user_id"), primary_key=True, nullable=False)
    trackers = db.relationship("User", secondary="relation_master")

class Relations(db.Model):
    __tablename__ = 'relation_master'
    relation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer,   db.ForeignKey("user_master.user_id"), primary_key=True, nullable=False)
    tracker_id = db.Column(db.Integer,  db.ForeignKey("tracker_master.tracker_id"), primary_key=True, nullable=False) 
    log_id = db.Column(db.Integer,  db.ForeignKey("log_master.log_id"), primary_key=True, nullable=False)

class Logs(db.Model):
    __tablename__ = 'log_master'
    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.String, nullable = False)
    notes = db.Column(db.String, nullable = False)
    user_id = db.Column(db.Integer,   db.ForeignKey("user_master.user_id"), primary_key=True, nullable=False)
    log_time = db.Column(db.DateTime, nullable = False)  
    # users = db.relationship("User", secondary="relation_master")
    # trackers = db.relationship("Tracker", secondary="relation_master")

