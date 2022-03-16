from flask_sqlalchemy import SQLAlchemy
from application.models import *




#To get all user names
def user_check_name():
    usernames = db.session.query(User.user_name).all()
    return usernames


#To get all user names and email
def user_check_email():
    useremail = db.session.query(User.user_email).all()
    return useremail